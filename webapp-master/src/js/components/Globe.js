import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import Viewer from "cesium/Source/Widgets/Viewer/Viewer";
import BingMapsImageryProvider from "cesium/Source/Scene/BingMapsImageryProvider";
import CesiumTerrainProvider from "cesium/Source/Core/CesiumTerrainProvider";
import Cartesian3 from "cesium/Source/Core/Cartesian3";
// import { Cesium } from "cesium/Source/Cesium";
import axios from "axios";
import { addPoints, setTime } from "../actions";

import "cesium/Source/Widgets/widgets.css";
import buildModelUrl from "cesium/Source/Core/buildModuleUrl";
buildModelUrl.setBaseUrl('./static/cesium');

const BING_MAPS_URL = "//dev.virtualearth.net";
const BING_MAPS_KEY = "ApDPY15x9lCXO5Hw89M1G5Q84_BlKalPbjor8GvKGj2UAnVtzlT5UT-zrylU1e48";
// const STK_TERRAIN_URL = "//assets.agi.com/stk-terrain/world";

require('../../css/globe.css');
// require('cesium/Widgets/widgets.css');
var Cesium = require('cesium');
// var Viewer = require('cesium/Widgets/Viewer/Viewer');
// var BingMapsImageryProvider = require('cesium/Scene/BingMapsImageryProvider');
// var CesiumTerrainProvider = require('cesium/Core/CesiumTerrainProvider');
// var Cartesian3 = require('cesium/Core/Cartesian3');
// var buildModelUrl = require('cesium/Core/buildModuleUrl');
// buildModelUrl.setBaseUrl('./static/cesium');

class Globe extends React.Component {

	constructor() {
		super();
		this.state = {
			t: null,
			drawn: false,
			flag: false,
			hostname: 'http://127.0.0.1:5000'
		};
	}

	componentDidMount() {
		Cesium.Ion.defaultAccessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmZDdmMDg5MS00MjQwLTRlMDUtOTRiZi0yZmVkNDFjMTFmMDQiLCJpZCI6ODAxNywic2NvcGVzIjpbImFzciIsImdjIl0sImlhdCI6MTU1MTA1MjI5N30.TewDjS5FlMse_gZAWyWhQ8ngnHRu_HgTCBvHl8ECS9g";
		const imageryProvider = new BingMapsImageryProvider({
            url : BING_MAPS_URL,
            key : BING_MAPS_KEY,
        });
		const terrainProvider = new CesiumTerrainProvider({
			url: Cesium.IonResource.fromAssetId(1)
		});
		this.viewer = new Viewer(this.cesiumContainer, {
            shouldAnimate: true,
            baseLayerPicker : false,
            fullscreenButton : false,
            geocoder : false,
            homeButton : false,
            infoBox : false,
            sceneModePicker : false,
            selectionIndicator : true,
            timeline : false,
            navigationHelpButton : false,
            scene3DOnly : true,
            imageryProvider,
            terrainProvider,
			requestRenderMode: true,
        });

		this.setState({t: setInterval(() => this.updatePosition(), 20)});
	}

	updatePosition() {
		if (this.state.flag === false) {
			this.state.flag = true;
			let dTime = this.julianIntToDate(this.runFunction());
			this.props.setTime(dTime);
			if (dTime) {
				axios.post(this.state.hostname + '/api/satellite', {'time': dTime})
					.then(response => {
						this.props.addPoints(response.data.satellites, response.data.lines, response.data.stations);
						this.state.flag = false;
					});
			}
		}
	}

	julianIntToDate(julianDate) {
		if (julianDate) {
			let date = julianDate.dayNumber;
			let time = julianDate.secondsOfDay;

			let y = 4716;
			let v = 3;
			let j = 1401;
			let u =  5;
			let m =  2;
			let s =  153;
			let n = 12;
			let w =  2;
			let r =  4;
			let B =  274277;
			let p =  1461;
			let C =  -38;
			let f = date + j + Math.floor((Math.floor((4 * date + B) / 146097) * 3) / 4) + C;
			let e = r * f + v;
			let g = Math.floor((e % p) / r);
			let h = u * g + w;
			let D = Math.floor((h % s) / u) + 1;
			let M = ((Math.floor(h / s) + m) % n) + 1;
			let Y = Math.floor(e / p) - y + Math.floor((n + m - M) / n) ;

			let H = time / 3600;
			let mm = (H % 1) * 60;
			let S = time % 60;
			return new Date(new Date(Y, M - 1, D, Math.floor(H), Math.floor(mm), S).getTime() + (6 * 60 * 60000) - 37000);
		}
	}

	componentWillUnmount() {
        if(this.viewer) {
            this.viewer.destroy();
        }
        clearInterval(this.state.t);
    }

    addPointsToGlobe(point) {
		this.viewer.entities.removeAll();
		point.forEach(point => this.viewer.entities.add({
			id: point.id,
			position: Cartesian3.fromDegrees(point.longitude, point.latitude, point.height),
			point: { pixelSize: point.size }
		}));
    }

    addPointOnGlobe(point) {
		let set = false;
	    let values = this.viewer.entities.values.length;
	    for (let i = 0; i < values; i++) {
		    if (this.viewer.entities.values[i].id === point.id) {
			    this.viewer.entities.values[i].position = this.handlePositionChange(point);
			    set = true;
			    break;
		    }
	    }
	    if (!set) {
	        let entity = this.viewer.entities.add(this.generateEntity(point));
	        entity.position = this.handlePositionChange(point);
	    }
    }

    handlePositionChange(point) {
		return Cartesian3.fromDegrees(point.longitude, point.latitude, point.height);
    }

    removeCesiumEntityById(id) {
		let values = this.viewer.entities.values;
		let remove = -1;
		for (let i = 0; i < values.length; i++) {
			if (values[i].id === id) {
				remove = i;
				break;
			}
		}
		if (remove !== -1) {
			this.viewer.entities.remove(values[remove]);
		}
    }

    removeEntitiesByIndex(indices) {
		indices.forEach(index => this.viewer.entities.remove(index));
    }

    generateEntity(point) {
		return {
			id: point.id,
			point: { pixelSize: point.size }
		}
    }

    addLinesOnGlobe(lines) {
		let ids = this.viewer.entities.values.map(value => value['id']).filter(id => id.startsWith('line-'));
		console.log(ids);
		lines.forEach(line => {
			console.log(line['id']);
			if (!ids.includes('line-' + line['id'])) {
				this.viewer.entities.add({
					id: 'line-' + line['id'],
					polyline: {
						show: true,
						width: 2.0,
						arcType: Cesium.ArcType.NONE,
						positions: new Cesium.PositionPropertyArray([
							new Cesium.ReferenceProperty(this.viewer.entities, line['id'].split('|')[0], ['position']),
							new Cesium.ReferenceProperty(this.viewer.entities, line['id'].split('|')[1], ['position']),
						]),
						material: new Cesium.ColorMaterialProperty(Cesium.Color.RED.withAlpha(0.25))
					}
				});
			}
			ids = ids.filter(function(value, index, arr) {
					return value !== 'line-' + line['id'];
				});
		});
		ids.forEach(id => this.removeCesiumEntityById(id));
    }

    runFunction() {
		if (this.viewer) {
			return this.viewer.clock.currentTime;
		}
		return null;
    }


	render() {
		const containerStyle = {
            width: '100%',
            height: '100%',
            display : "flex",
            alignItems : "stretch",
        };

        const widgetStyle = {
            flexGrow : 2
        };

        const { satellites, lines, stations } = this.props;
        if (this.viewer && satellites) {
        	// this.addPointsToGlobe(satellites);
	        satellites.forEach(point => this.addPointOnGlobe(point));
	        stations.forEach(point => this.addPointOnGlobe(point));
	        if (lines) {
		        this.addLinesOnGlobe(lines);
	        }
        }

        return (
        	<div className='cesium-root'>
	            <div className="cesiumGlobeWrapper" style={containerStyle}>
	                <div
	                    className="cesiumWidget"
	                    ref={ element => this.cesiumContainer = element }
	                    style={widgetStyle}>
	                </div>
	            </div>
	        </div>
        );
    }
}

Globe.propTypes = {

};

function mapStateToProps(state) {
	return {
		satellites: state.globe.satellites,
		stations: state.globe.stations,
		lines: state.globe.lines,
	}
}

function mapDispatchToProps(dispatch) {
	return {
		addPoints: (satellites, lines, stations) => dispatch(addPoints(satellites, lines, stations)),
		setTime: time => dispatch(setTime(time))
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(Globe);