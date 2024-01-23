
import { Navigation } from '../Navigation/Navigation';
import { Component } from "react";
import './Grafana.css';
import Iframe from 'react-iframe';

export class Grafana extends Component {
    grafanaURL = 'http://localhost:3000/d/dced5fb4-e93d-40d2-96bb-85bc7270a2d5/odbrana-3?orgId=1&from=1705938632179&to=1705960232179&theme=light&viewPanel=1&fullscreen&kiosk';
    constructor(props) {
        super(props);
    }

    extractDeviceIdFromUrl() {
        const parts = window.location.href.split('/');
        return parts[parts.length - 1];
    }

    render() {
        return (
            <div>
                <Navigation></Navigation>
                {/* <iframe src="http://localhost:3000/d-solo/dced5fb4-e93d-40d2-96bb-85bc7270a2d5/odbrana-3?orgId=1&from=1705939217638&to=1705960817638&panelId=2&theme=light" width="100%" height="600px" frameborder="0"></iframe> */}
                <iframe src="http://localhost:3000/d-solo/a8c1a5da-f2e0-4d33-b1e4-5f62c6c93c46/new-dashboard?orgId=1&from=1706012788290&to=1706013088290&theme=light&panelId=1" width="100%" height="600px" frameborder="0"></iframe>
            </div>
        )
    }
};