import React, { Component } from "react";
import './Devices.css';
import { Navigation } from "../Navigation/Navigation";
import { Divider } from '@mui/material';
import Dialog from "../Dialog/Dialog";
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
            topics: [],
            showAlarmDialog: true,
        };
        this.id = 1;
    }

    handlePinInput = async() => {
        // TODO: not implemented yet
        await this.setState({showAlarmDialog: false});
    }
    
    async componentDidMount() {
        try {
            const data = await DeviceServices.getDevices(this.state.selectedPi);
            const initialData = data.map(device => ({ Name: device, Value: [] }));
            this.setState({ data: initialData });

            const topics = await DeviceServices.getTopics(this.state.selectedPi);
            this.setState({ topics: topics });
            //console.log(topics)
        } catch (error) {
            console.error('Error fetching data:', error);
        }

        // MQTT
        const mqttClient = mqtt.connect('ws://localhost:9001');

        this.state.topics.forEach(topic => {
            mqttClient.subscribe(topic, function (err) {
                if (!err) {
                    console.log(`Pretplaceni ste na topic: ${topic}`);
                }
            });
        });
        
        mqttClient.on('message', this.handleMqttMessage);
    }

    setB4SD = (data) => {
        const hasB4SD = data.some(device => device.Name === 'B4SD');
        const currentTime = new Date().toLocaleTimeString();
        const b4sdIndex = data.findIndex(device => device.Name === 'B4SD');
        if (b4sdIndex !== -1) {
            const timeIndex = data[b4sdIndex].Value.findIndex(v => v.name === 'time');
            if (timeIndex === -1) {
                data[b4sdIndex].Value.push({ name: 'time', value: currentTime });
            } else {
                data[b4sdIndex].Value[timeIndex].value = currentTime;
            }
        }

        return data
    }

    handleMqttMessage = (topic, message) => {
        // console.log(message.toString());

        const parsedMessage = JSON.parse(message.toString());

        // console.log(this.state.data)
        const updatedData = [...this.state.data];
        this.setB4SD(updatedData)

        const deviceIndex = updatedData.findIndex(device => device.Name === parsedMessage.measurement);
    
        try {
            // Ako uređaj već postoji, pronađite vrednost unutar njega prema imenu
            const valueIndex = updatedData[deviceIndex].Value.findIndex(v => v.name === parsedMessage.name);
            let value = parsedMessage.value;

            if (valueIndex === -1) {
                // Ako vrednost za dato ime ne postoji, dodajte je
                console.log(parsedMessage.value)
                // console.log(typeof(parsedMessage.value))
                
                if (typeof(parsedMessage.value) == "object") {
                    console.log("usloooo")
                    console.log(parsedMessage.value)
                    value = Object.entries(value)
                    .map(([key, v]) => `${key}: ${v}`)
                    .join('\n');
                }
                else 
                    value = value.toString()
                updatedData[deviceIndex].Value.push({ name: parsedMessage.name, value: value });
            } else {
                if (typeof(parsedMessage.value) == "object") {
                    console.log("usloooo")
                    //console.log(parsedMessage.value)
                    value = Object.entries(value)
                    .map(([key, v]) => `${key}: ${v}`)
                    .join('\n');
                    console.log(value)
                }
                else 
                    value = value.toString()
                // Ako vrednost već postoji, ažurirajte je
                updatedData[deviceIndex].Value[valueIndex].value = value;
            }

            this.setState({ data: updatedData });
        } catch(err) {}    
    }

    updateSelectedPi = async (newPi) => {
        const updatedData = this.state.data.map(device => ({ Name: device.Name, Value: [] }));
        this.setState({ selectedPi: newPi, data: updatedData });

        // logout from old topics
        const mqttClient = mqtt.connect('ws://localhost:9001');
        this.state.topics.forEach(topic => {
            mqttClient.unsubscribe(topic, function (err) {
                if (!err) {
                    // console.log(`Odjavljeni ste sa topica: ${topic}`);
                }
            });
        });

        try {
            const data = await DeviceServices.getDevices(newPi);
            const initialData = data.map(device => ({ Name: device, Value: [{name: '', value: ''}] }));
            this.setState({ data: initialData });

            const topics = await DeviceServices.getTopics(newPi);
            this.setState({ topics: topics });

            // subscribe on new topics
            topics.forEach(topic => {
                mqttClient.subscribe(topic, function (err) {
                    if (!err) {
                        // console.log(`Pretplaceni ste na topic: ${topic}`);
                    }
                });
            });
            
            mqttClient.on('message', this.handleMqttMessage);
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
                    <span className='estate-title'>{this.state.selectedPi}</span>
                    <Divider style={{ width: "87%", marginLeft: 'auto', marginRight: 'auto', marginBottom: '20px' }} />
                    <DevicesList devices={this.state.data}/>
                </div>
                {this.state.showAlarmDialog && (
                    <Dialog
                        title="ALARM"
                        message="Please input PIN to stop the alarm."
                        onConfirm={this.handlePinInput}
                        // onCancel={this.handleCancel}
                        isDiscard={true}
                        inputPlaceholder="Write PIN here..."
                    />
                )}
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
                                    <div key={valueIndex}>
                                        <span className='device-text'>{value.name}</span>
                                        <span className='device-value'>{value.value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
