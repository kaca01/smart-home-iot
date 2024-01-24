import React, { useState } from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import Snackbar from '@mui/material/Snackbar';

const ColorDialog = ({ isOpen, onClose, onColorSelect }) => {
    const colors = [
        { name: 'Turn off', value: 'black', button: '0' },
        { name: 'Red', value: 'red', button: "2" },
        { name: 'Yellow', value: 'yellow', button: "5" },
        { name: 'White', value: 'white', button: "1" },
        { name: 'Green', value: 'green', button: "3" },
        { name: 'Blue', value: 'blue', button: "4" },
        { name: 'Purple', value: 'purple', button: "6" },
        { name: 'Light Blue', value: 'lightblue', button: "7" },
    ];

    const [currentColor, setCurrentColor] = useState(null);
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    const handleColorButtonClick = async (color) => {
        setCurrentColor(color);
        console.log(color)
        setSnackbarOpen(true); 
        
        try {
            const apiUrl = 'http://localhost:5000/api/bir_button';
        
            const data = { "button":  color.button };
        
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            };
        
            // Izvršite HTTP zahtev
            const response = await fetch(apiUrl, options);
        
            // Proverite status odgovora
            if (response.ok) {
                console.log('Podaci uspešno poslati na backend.');
              // Ovde možete dodati dalju logiku nakon uspešnog slanja podataka
            } else {
                console.error('Došlo je do greške prilikom slanja podataka na backend.');
            }
        } catch (error) {
                console.error('Došlo je do greške:', error);
        } 
    };

    const handleSnackbarClose = () => {
        setSnackbarOpen(false);
    };

    return (
        <>
        <Dialog  
        open={isOpen}   
        onClose={onClose}  
        contentLabel="Color Dialog"
        >
        <DialogTitle>Choose a color</DialogTitle>
        <DialogContent dividers>
            <div className="color-buttons">
            {colors.map((color, index) => (
                <Button
                key={index}
                variant="outlined"
                style={{ backgroundColor: color.value, color: color.value === 'white' ? 'black' : 'white', marginRight: '10px' }}
                onClick={() => handleColorButtonClick(color)}
                >
                {color.name}
                </Button>
            ))}
            </div>
        </DialogContent>
        <DialogActions>
            <Button onClick={onClose}>Cancel</Button>
        </DialogActions>
        </Dialog>

        <Snackbar
        open={snackbarOpen}
        autoHideDuration={1000}
        onClose={handleSnackbarClose}
        message="You changed rgb!"
        />
        </>
    );
};

export default ColorDialog;
