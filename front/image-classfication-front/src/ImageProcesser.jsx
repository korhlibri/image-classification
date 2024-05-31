import React, { useState } from "react";
import Tab from 'react-bootstrap/Tab'
import Tabs from 'react-bootstrap/Tabs'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

export default function Formulario () {
    const [selectedFile, setSelectedFile] = useState(null);
    const [base64Image, setBase64Image] = useState('');
    const [urlImage, setUrlImage] = useState('');
    const [responseData, setResponseData] = useState(null);
    const [fileName, setFileName] = useState('Choose file');
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (event) => {
        if (event.target.files.length > 0) {
            setFileName(event.target.files[0].name);
        } else {
            setFileName('Choose file');
        }
        const file = event.target.files[0];
        if (file) { 
        const reader = new FileReader();
        reader.onloadend = () => {
            
            var base64result = reader.result.split(',')[1];
            setBase64Image(base64result);
        };
        reader.readAsDataURL(file);
        setSelectedFile(file)
        }
    };

    const handleSubmitFile = (event) => {
        
        event.preventDefault();
        

        if (!selectedFile) {
        alert('Select a File');
        return;
        }

        const apiUrl = 'http://127.0.0.1:5000/image'

        fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image: base64Image,
        }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success', data);
            setResponseData(data);
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    };



    const handleSubmitUrl = (event) => {
        event.preventDefault();
        setIsLoading(true);

        if (urlImage === '') {
            alert('Enter an URL');
            setIsLoading(false);
            return;
        }


        const apiUrl = 'http://127.0.0.1:5000/url'

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: urlImage,
            }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success', data);
                setResponseData(data);
                setIsLoading(false);
            })
            .catch((error) =>{
                console.error('Error:', error);
            });
            
        }
        
    return(
    <div>
        <Tabs
        defaultActiveKey="form-file"
        className="mb-3"
        fill
        >
            <Tab eventKey="form-file" title="File">
                <Form onSubmit={handleSubmitFile}>
                    <Form.Group controlId="formFile" className="mb-3">
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                            id="customFileInput"
                        />
                        <Button variant="outline-primary" onClick={() => document.getElementById('customFileInput').click()}>
                            {fileName}
                        </Button>
                    </Form.Group>
                    <Button type="submit">Send</Button>
                </Form>
            </Tab>
            <Tab eventKey="form-url" title="Url">
                <Form onSubmit={handleSubmitUrl}>
                    <Form.Group className="mb-3">
                        <Form.Control type="url" value={urlImage}
                        onChange={(e) => setUrlImage(e.target.value)}/>
                    </Form.Group>
                    <Button type="submit" disabled={isLoading}>Send</Button>
                    {
                        isLoading && (
                            <Spinner animation="border" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </Spinner>
                        )
                    }
                </Form>
            </Tab>
        </Tabs>
        <hr />
        <div className="imPr-results">
            <h1>Content Results</h1>
            {responseData && (
                    <div>
                        <div>
                            <Row>
                                <Col><p>Adult : {responseData.data.adult.percentage.toFixed(2)}% </p></Col>
                                <Col><p>Total amount of images: {responseData.data.adult.amount}</p></Col>
                            </Row>
                            <Row>
                                <Col><p>Medical : {responseData.data.medical.percentage.toFixed(2)}% </p></Col>
                                <Col><p>Total amount of images: {responseData.data.medical.amount}</p></Col>
                            </Row>
                            <Row>
                                <Col><p>Violent : {responseData.data.violent.percentage.toFixed(2)}% </p></Col>
                                <Col><p>Total amount of images: {responseData.data.violent.amount}</p></Col>
                            </Row>
                        </div>
                    </div>
                )}
        </div>
        
    </div>
    )
}