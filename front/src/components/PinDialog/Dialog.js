import React, { useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const PinInputDialog = ({ open, onClose }) => {
  const [numbers, setNumbers] = useState(['', '', '', '']);

  const handleInputChange = (index, value) => {
    const newNumbers = [...numbers];
    newNumbers[index] = value;
    setNumbers(newNumbers);
  };

  const handleSave = async () => {
    // Ovde možete dodati logiku za čuvanje unetih brojeva
    // Na primer, pozovite neku funkciju koja će obraditi ove brojeve
    console.log('Uneti brojevi:', numbers.join(''));

    const pin = numbers.join('');

    try {
        const apiUrl = 'http://localhost:5000/api/send_pin';
    
        const data = { pin: pin };

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
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>INPUT PIN</DialogTitle>
      <DialogContent>
        <div style={{ display: 'flex', gap: '50px' }}>
            {numbers.map((number, index) => (
            <TextField
                key={index}
                label={`Num ${index + 1}`}
                variant="outlined"
                size='small'
                value={number}
                inputProps={{ maxLength: 1 }}
                onChange={(e) => handleInputChange(index, e.target.value)}
                margin="normal"
            />
            ))}
        </div>
      </DialogContent>
      <DialogActions>
        <Button style={{color: "red", fontSize: "larger"}} onClick={onClose}>CLOSE</Button>
        <Button style={{color: "green", fontSize: "larger"}} onClick={handleSave}>OK</Button>
      </DialogActions>
    </Dialog>
  );
};

export default PinInputDialog;
