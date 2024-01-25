
import { Navigation } from '../Navigation/Navigation';
import { Component } from "react";
import './Grafana.css';
import Iframe from 'react-iframe';

export class Grafana extends Component {
    // grafanaURL = 'http://localhost:3000/d/dced5fb4-e93d-40d2-96bb-85bc7270a2d5/odbrana-3?orgId=1&from=1705938632179&to=1705960232179&theme=light&viewPanel=1&fullscreen&kiosk';
    urls = ["http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127304649&to=1706127305290&theme=light&panelId=2",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127304649&to=1706127305290&theme=light&panelId=3",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127304649&to=1706127305290&theme=light&panelId=1",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706126121105&to=1706127305031&theme=light&panelId=4",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706126121105&to=1706127305031&theme=light&panelId=5",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706126121105&to=1706127305031&theme=light&panelId=6",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706126121105&to=1706127305031&theme=light&panelId=7",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706126121105&to=1706127305031&theme=light&panelId=8",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706126986541&to=1706130586542&theme=light&panelId=9",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127219117&to=1706130819118&theme=light&panelId=10",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127381056&to=1706130981056&theme=light&panelId=11",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127506219&to=1706131106219&theme=light&panelId=12",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706127725523&to=1706131325523&theme=light&panelId=13",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706128094266&to=1706131694266&theme=light&panelId=14",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706128238736&to=1706131838736&theme=light&panelId=15",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706128482442&to=1706132082442&theme=light&panelId=16",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706128628041&to=1706132228041&theme=light&panelId=17",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706128743684&to=1706132343684&theme=light&panelId=18",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706133493424&to=1706137093424&theme=light&panelId=19",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706133718491&to=1706137318491&theme=light&panelId=20",
    "http://localhost:3000/d-solo/f1079d2a-d46f-4c7b-807b-24042bda0500/odbrana-3?orgId=1&from=1706137710665&to=1706138010665&theme=light&panelId=21"];
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
        } else if (device == "dl") {
            return this.urls[1];
        }
        else if (device == "dus1") {
            return this.urls[2];
        }
        else if (device == "dht1") {
            return this.urls[3];
        }
        else if (device == "dht2") {
            return this.urls[4];
        }
        else if (device == "pir1") {
            return this.urls[5];
        }
        else if (device == "pir2") {
            return this.urls[6];
        }
        else if (device == "dms") {
            return this.urls[7];
        }
        else if (device == "dpir1") {
            return this.urls[8];
        }
        else if (device == "ds1") {
            return this.urls[9];
        }
        else if (device == "dpir2") {
            return this.urls[10];
        }
        else if (device == "gdht") {
            return this.urls[11];
        }
        else if (device == "pir3") {
            return this.urls[12];
        }
        else if (device == "dht3") {
            return this.urls[13];
        }
        else if (device == "dus2") {
            return this.urls[14];
        }
        else if (device == "ds2") {
            return this.urls[15];
        }
        else if (device == "pir4") {
            return this.urls[16];
        }
        else if (device == "dht4") {
            return this.urls[17];
        }
        else if (device == "bir") {
            return this.urls[18];
        }
        else if (device == "rgb") {
            return this.urls[19];
        }
        else if (device == "alarm") {
            return this.urls[20];
        }
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