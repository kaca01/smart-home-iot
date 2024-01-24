
import { Navigation } from '../Navigation/Navigation';
import { Component } from "react";
import './Grafana.css';
import Iframe from 'react-iframe';

export class Grafana extends Component {
    grafanaURL = 'http://localhost:3000/d/dced5fb4-e93d-40d2-96bb-85bc7270a2d5/odbrana-3?orgId=1&from=1705938632179&to=1705960232179&theme=light&viewPanel=1&fullscreen&kiosk';
    urls = ["http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127335948&to=1706127606574&theme=light&panelId=2"];
    constructor(props) {
        super(props);
        this.state = {
            device: '',
        };
    }

    async componentDidMount() {
        await this.setState({device: this.extractDeviceIdFromUrl()});
        console.log("Device: ", this.state.device);
    }

    extractDeviceIdFromUrl() {
        const parts = window.location.href.split('/');
        return parts[parts.length - 1];
    }

    getUrl(device) {
        if (device == "gsg") {
            return this.urls[0];
        }// TODO: else if bla bla
    }

    render() {
        return (
            <div>
                <Navigation></Navigation>
                {/* <iframe src="http://localhost:3000/d-solo/dced5fb4-e93d-40d2-96bb-85bc7270a2d5/odbrana-3?orgId=1&from=1705939217638&to=1705960817638&panelId=2&theme=light" width="100%" height="600px" frameborder="0"></iframe> */}
                <iframe src={this.getUrl(this.state.device)} width="100%" height="600px" frameborder="0"></iframe>
            </div>
        )
    }
};