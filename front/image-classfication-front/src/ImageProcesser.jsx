import React, { useState } from "react";
import { userState } from 'react';

export default function Formulario () {
    const [selectedFile, setSelectedFile] = useState(null);
    const [base64Image, setBase64Image] = useState('');
    const [urlImage, setUrlImage] = useState('')

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) { 
        const reader = new FileReader();
        reader.onloadend = () => {
            setBase64Image(reader.result);
        };
        reader.readAsDataURL(file);
        setSelectedFile(file)
        }
    };

    const handleSubmitFile = (event) => {
        
        event.preventDefault();

        if (!selectedFile) {
        alert('Seleccione una imagen primero');
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
        })
        .catch((error) =>{
            console.error('Error:', error);
        });
    };



    const handleSubmitUrl = (event) => {
        event.preventDefault();

        if (urlImage === '') {
            alert('Introduzca una url');
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
            })
            .catch((error) =>{
                console.error('Error:', error);
            });
    }

    return(
        <div>
        <h1>FILE</h1>
        <form onSubmit={handleSubmitFile}>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
          />
          <button type="submit">Enviar</button>
        </form>
        <h1>URL</h1>
        <form onSubmit={handleSubmitUrl}>
          <input
            type="url"
            value={urlImage}
            onChange={(e) => setUrlImage(e.target.value)}
          />
          <button type="submit">Enviar</button>
        </form>
      </div>
    )
}