import { Component } from "react";
import './Devices.css';
import { Navigation } from "../Navigation/Navigation";
import { Divider } from '@mui/material';
import DeviceServices from "../../services/DeviceServices";
import mqtt from 'mqtt'


export class Devices extends Component {
    grafanaGraphUrl = 'http://localhost:3000/goto/oRkeFXcIR?orgId=1';
    grafanaSnapshotUrl = '<iframe src="http://localhost:3000/dashboard/snapshot/AFBGQisZEIFeSJ2zoKiEokiYgZE7Wnm8"></iframe>';
    constructor(props) {
        super(props);
        this.state = {
            selectedPi: 'PI1',
            data: [{
                "Name": "PIR1",
                "Value": "No motion detected",
            }, 
            {
                "Name": "PIR2",
                "Value": "Motion detected",
            },
            {
                "Name": "Door buzzer",
                "Value": "Buzzing!!!",
            },
            {
                "Name": "Door membrane switch",
            },
            {
                "Name": "Door light",
                "Value": "ON",
            },
            {
                "Name": "Door sensor 1",
                "Value": "The door is locked.",
            },
            {
                "Name": "Door ultrasonic sensor",
                "Value": "Someone entering",
            },
            ],
        };
        this.id = 1;
    }

    async componentDidMount() {
        try {
            const data = await DeviceServices.getDevices(this.state.selectedPi);
            console.log(data)
            // this.setState({ data: data || [] });
        } catch (error) {
            console.error('Error fetching data:', error);
        }

        // MQTT
        const mqttClient = mqtt.connect('ws://localhost:9001');

        const topicsToSubscribe = ['TEMP1', 'HMD1'];
            topicsToSubscribe.forEach(topic => {
                mqttClient.subscribe(topic, function (err) {
                    if (!err) {
                        console.log(`Pretplaceni ste na topic: ${topic}`);
                    }
                });
            });

            // Osluškivanje poruka
            mqttClient.on('message', function (topic, message) {
                console.log(`Dobijena poruka na topic-u ${topic}: ${message.toString()}`);
            });
    }

    render() {
        return (
            <div>
                <Navigation></Navigation>
                <div id="panel">
                    {/* <Iframe url={this.grafanaGraphUrl} width="100%" height="600px"/> */}
                    <span className='estate-title'>PI {this.id}</span>
                    <Divider style={{ width: "87%", marginLeft: 'auto', marginRight: 'auto', marginBottom: '20px' }} />
                    <DevicesList devices={this.state.data}/>
                </div>
            </div>
        )
    }
}

const DevicesList = ({ devices }) => {
    const chunkSize = 5; // Number of items per row

    const chunkArray = (arr, size) => {
        return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
            arr.slice(i * size, i * size + size)
        );
    };

    const rows = chunkArray(devices, chunkSize);

    return (
        <div id='devices-container'>
            {rows.map((row, rowIndex) => (
                <div key={rowIndex} className='device-row'>
                    {row.map((device, index) => (
                        <div key={index} className='device-card'>
                            <div className='device-info'>
                                <p className='device-title'>{device.Name}</p>
                                <p className='device-text'>{device.Value}</p>
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
