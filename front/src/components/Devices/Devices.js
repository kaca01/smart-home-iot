import { Component } from "react";
import './Devices.css';
import Iframe from 'react-iframe';
import { Navigation } from "../Navigation/Navigation";


export class Devices extends Component {
    grafanaGraphUrl = 'http://localhost:3000/goto/oRkeFXcIR?orgId=1';
    grafanaSnapshotUrl = '<iframe src="http://localhost:3000/dashboard/snapshot/AFBGQisZEIFeSJ2zoKiEokiYgZE7Wnm8"></iframe>';
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Navigation></Navigation>
                <div id="panel">
                    <Iframe url={this.grafanaGraphUrl} width="100%" height="600px"/>
                    <p>Welcome to Devices page!</p>
                </div>
            </div>
        )
    }
}
