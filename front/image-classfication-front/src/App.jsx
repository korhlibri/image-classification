import "./App.css";
import HeaderNav from "./HeaderNav";
import Formulario from "./ImageProcesser";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Navbar';

export function App() {
  return (
    <>
      <style type="text/css">
        {`
      .navbar-header {
        background-color: #472DB1;
        color: white;
        padding: 20px;
      }
      `}
      </style>

      <Navbar variant="header">
        <Container>
          <HeaderNav/>
        </Container>
      </Navbar>
      
      <Container className="texto">
        <Formulario/>
      </Container>
      
      
    </>
  );
}