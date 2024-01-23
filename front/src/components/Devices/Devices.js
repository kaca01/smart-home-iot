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
            data: [],
        };
        this.id = 1;
    }

    async componentDidMount() {
        try {
            const data = await DeviceServices.getDevices(this.state.selectedPi);
            const initialData = data.map(device => ({ Name: device, Value: [] }));
            this.setState({ data: initialData });
        } catch (error) {
            console.error('Error fetching data:', error);
        }

        // MQTT
        const mqttClient = mqtt.connect('ws://localhost:9001');

        const topicsToSubscribe = ['TEMP1', 'HMD1', 'MOTION1'];
            topicsToSubscribe.forEach(topic => {
                mqttClient.subscribe(topic, function (err) {
                    if (!err) {
                        console.log(`Pretplaceni ste na topic: ${topic}`);
                    }
                });
            });
            
            mqttClient.on('message', this.handleMqttMessage);
    }

    handleMqttMessage = (topic, message) => {
        console.log(message.toString());

        const parsedMessage = JSON.parse(message.toString());
    
        const updatedData = [...this.state.data];
    
        const deviceIndex = updatedData.findIndex(device => device.Name === parsedMessage.name);
        console.log(deviceIndex)
        console.log(updatedData)
    
        if (deviceIndex === -1) {
            updatedData.push({
                Name: parsedMessage.name,
                Values: [parsedMessage.value],
            });
        } else {
            let value = parsedMessage.value;
            if (!value) value = true
            updatedData[deviceIndex].Value.push(value.toString());
            // // Ako je uređaj pronađen, proverite da li postoji svojstvo Values
            // if (!updatedData[deviceIndex].hasOwnProperty('Value')) {
            //     // Ako ne postoji, dodajte novo svojstvo Values sa vrednošću
            //     console.log("ne postoji")
            //     updatedData[deviceIndex].Value = [parsedMessage.value];
            // } else {
            //     // Ako postoji, ažurirajte njegovu listu vrednosti
            //     console.log("vec postoji")
                
                
            // }
        }
    
        this.setState({ data: updatedData });
    }

    updateSelectedPi = async (newPi) => {
        const updatedData = this.state.data.map(device => ({ Name: device.Name, Value: [] }));
        this.setState({ selectedPi: newPi, data: updatedData });
        try {
            const data = await DeviceServices.getDevices(newPi);
            const initialData = data.map(device => ({ Name: device, Value: [] }));
            this.setState({ data: initialData });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    render() {
        return (
            <div>
                <Navigation updateSelectedPi={this.updateSelectedPi}></Navigation>
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
                                {device.Value.map((value, valueIndex) => (
                                    <p key={valueIndex} className='device-text'>{value}</p>
                                ))}
                                {/* <p className='device-text'>{device.Value}</p> */}
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
