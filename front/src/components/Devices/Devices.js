import { Component } from "react";
import './Devices.css';
import { Navigation } from "../Navigation/Navigation";
import { Divider } from '@mui/material';
import PinInputDialog from "../PinDialog/Dialog";
import ColorDialog from "../RGBDialog/RGBDialog";


export class Devices extends Component {
    grafanaGraphUrl = 'http://localhost:3000/goto/oRkeFXcIR?orgId=1';
    grafanaSnapshotUrl = '<iframe src="http://localhost:3000/dashboard/snapshot/AFBGQisZEIFeSJ2zoKiEokiYgZE7Wnm8"></iframe>';
    constructor(props) {
        super(props);
        this.state = {
            isPinDialogOpen: false,
            isColorDialogOpen: false,
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

    updateSelectedPi = async (newPi) => {
        this.setState({ selectedPi: newPi });
    }

    // pin dialog
    handleOpenPinDialog = () => {
        this.setState({ isPinDialogOpen: true });
    };

    handleClosePinDialog = () => {
        this.setState({ isPinDialogOpen: false });
    };

    // color dialog
    handleOpenColorDialog = () => {
        this.setState({ isColorDialogOpen: true });
    };

    handleCloseColorDialog = () => {
        this.setState({ isColorDialogOpen: false });
    };

    render() {
        return (
            <div>
                <Navigation updateSelectedPi={this.updateSelectedPi}></Navigation>
                <div id="panel">
                    {/* <Iframe url={this.grafanaGraphUrl} width="100%" height="600px"/> */}
                    <span className='estate-title'>{this.state.selectedPi}</span>
                    <span>
                        <button className="button button1" onClick={this.handleOpenPinDialog}>INPUT PIN</button>
                        {this.state.selectedPi === 'PI3' && (
                            <button className="button button2" onClick={this.handleOpenColorDialog}>CONTROL RGB</button>
                        )}
                    </span>
                    <Divider style={{ width: "87%", marginLeft: 'auto', marginRight: 'auto', marginBottom: '20px' }} />
                    <DevicesList devices={this.state.data}/>
                </div>

                 {/* Dialog for input pin */}
                {this.state.isPinDialogOpen && (
                    <PinInputDialog open={this.state.isPinDialogOpen} onClose={this.handleClosePinDialog} />
                )}

                {/* Dialog for rgb */}
                {this.state.isColorDialogOpen && (
                    <ColorDialog isOpen={this.state.isColorDialogOpen} onClose={this.handleCloseColorDialog} />
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
                                <p className='device-text'>{device.Value}</p>
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
