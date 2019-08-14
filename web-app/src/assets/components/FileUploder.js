import React from 'react';
import axios from 'axios';
import './FileUploader.scss';

class FileUploder extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      selectedFile : null,
      uploadPercentage:0, 
    }
  }


  fileSelectedHandler = event => {
    this.setState({
      selectedFile: event.target.files[0]
    })
    console.log(event.target.files[0].name)
  }

  fileUploadHandler = () => {
    const data = new FormData();
    data.append('file', this.state.selectedFile, this.state.selectedFile.name);
    axios.post('https://us-central1-docker-compose-validator-b3e56.cloudfunctions.net/uploadFile', data, {
      mode: 'cors',
      onUploadProgress: ProgressEvent => {
        var uploadPercentage = Math.round(ProgressEvent.loaded / ProgressEvent.total * 100)
        console.log('Uploaded: ' + uploadPercentage + '%')
        this.setState({ uploadPercentage })
      }
    })
      .then(res => {
        console.log(res);
      });
  }


  render() {
    return (
      <div className="uploadDialog">
      <input type="file" onChange={this.fileSelectedHandler}/>
      <button onClick={this.fileUploadHandler}>Upload</button>
      </div>
    );
  }
}

export default FileUploder;





/*
import React from 'react';

class FileUploder extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ imageURL: `http://localhost:5000/${body.file}` });
      });
    });
  }

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        
        <br />
        <div>
          <button>Upload</button>
        </div>
      </form>
    );
  }
}

export default FileUploder;
*/