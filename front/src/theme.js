import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#CCCCFF',
    },
    secondary: {
      main: '#192734',
    },
  },
  customStyles: {
    myCustomButton: {
      textTransform: 'none',
      fontFamily: 'Poppins',
      width: '37%',
    },
    // Add more custom styles as needed
  },
});

export default theme;