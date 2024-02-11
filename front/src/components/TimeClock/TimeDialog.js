import React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { Dialog } from '@mui/material';

const TimeInputDialog = ({ isOpen, onClose, onSubmit }) => {
    const [time, setTime] = React.useState('');

    const handleTimeChange = (event) => {
        setTime(event.target.value);
    };

    const handleSubmit = async () => {
        try {
            const apiUrl = 'http://localhost:5000/api/send_time';
        
            console.log(time)
            const data = { time: time };
    
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
            },
                body: JSON.stringify(data),
            };
        
            const response = await fetch(apiUrl, options);
    
            if (response.ok) {
              console.log('Podaci uspešno poslati na backend.');
            } else {
              console.error('Došlo je do greške prilikom slanja podataka na backend.');
            }
          } catch (error) {
            console.error('Došlo je do greške:', error);
          }

        onClose();
    };

    return (
        <Dialog
            open={isOpen}
            onClose={onClose}
            contentLabel="Time Input Dialog"
        >
            <DialogTitle>Enter Time</DialogTitle>
            <DialogContent dividers>
                <TextField
                    label="Time"
                    type="text"
                    value={time}
                    onChange={handleTimeChange}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={handleSubmit}>Submit</Button>
            </DialogActions>
        </Dialog>
    );
};

export default TimeInputDialog;
