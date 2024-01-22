import { Component } from "react";
import './Devices.css';
import Iframe from 'react-iframe';


export class Devices extends Component {
    grafanaGraphUrl = 'http://localhost:3000/d/dced5fb4-e93d-40d2-96bb-85bc7270a2d5/odbrana-3?orgId=1&from=1705923737720&to=1705927337720&viewPanel=1';
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <p>Welcome to Devices page!</p>
                <Iframe url={this.grafanaGraphUrl} width="100%" height="600px"/>
            </div>
        )
    }
}
