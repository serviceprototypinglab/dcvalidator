import React, {useMemo, useState} from 'react';
import axios from 'axios';
import {useDropzone} from 'react-dropzone';
import LinearProgress from '@material-ui/core/LinearProgress';
import { ReactComponent as YmlIcon } from '../img/icons/common/yml.svg';

import './FileUploader.scss';

const baseStyle = {
  // flex: 1,
  width: '64vh',
  height: '26vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 5,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  outline: 'none',
  transition: 'border .24s ease-in-out',
  cursor: 'pointer',
};

const activeStyle = {
  borderColor: '#2196f3'
};

const acceptStyle = {
  borderColor: '#00e676',
  backgroundColor: 'rgba(64, 119, 192, 0.025)',
};

const rejectStyle = {
  borderColor: '#ff1744',
  backgroundColor: 'rgba(192, 64, 64, 0.068)',
  cursor: 'not-allowed',
};

function StyledDropzone(props) {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
    
  } = useDropzone({
        onDrop: props.onDrop,
        accept: 'application/x-yaml, application/x-yaml',
        multiple: true,
      });

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? activeStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }),
    [isDragActive, isDragReject, isDragAccept]);

  return (
    <div className="container">
      <div {...getRootProps({style})}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop some files here, or click to select files</p>
      </div>
    </div>
  );
}



function FileUploder(props) {

      const [selectedFiles, SetSelectedFiles] = useState([])
      const [uploadPercentage,SetUploadPercentage] = useState(0)
      const [uploading,SetUploading] = useState(0) // 0: No    1: uploading    2: finished
      const [draged,SetDraged] = useState(false)
      

  const fileSelectedHandler = event => {
      let files =  selectedFiles
      event.map(file => {
        if (!(file in files)) {
          files.push(file)
        }
        return null
      })
      
      SetSelectedFiles(files)
      SetDraged(true)
  }

  const fileUploadHandler = () => {

    var data = new FormData();
    selectedFiles.map(file => data.append('file[]', file))
    // https://us-central1-docker-compose-validator-b3e56.cloudfunctions.net/uploadFile
    SetUploading(1)
    axios.post('http://localhost:5000/upload', data, { 
      mode: 'cors',
      onUploadProgress: ProgressEvent => {
        var uploadProgress = Math.round(ProgressEvent.loaded / ProgressEvent.total * 100)
        // console.log('Uploaded: ' + uploadPercentage + '%')
        SetUploadPercentage(uploadProgress)
      }
    })
      .then(res => {
        SetUploading(2)
        console.log(res);
      });
  }



    return (
      <div className="uploadDialog">
      <StyledDropzone onDrop={fileSelectedHandler} draged={draged} className="dropzone"/>
      <span style={{display: 'flex', justifyContent: 'flex-start', flexDirection: 'column', alignSelf: 'flex-start', width: '100%'}}>

      { selectedFiles &&
        
         selectedFiles.map(file => <div style={{marginTop: '25px', alignItems: 'center', flexDirection: 'row', display:'flex', justifyContent: 'space-between'}}>
        <span style={{display:'flex', alignItems: 'center', flexDirection: 'row',}}>
        <YmlIcon className='ymlIcon' />
        <span className='fileName'>
          {file.path}
        </span>
        </span>
      </div>)
      }
      </span>
      <span style={{width: '100%', marginTop: '25px'}}>
        { uploading !== 0 && <LinearProgress variant="determinate" value={ uploadPercentage} />}
      </span>
      { uploading === 0 &&  <button className="uploadButton" onClick={  fileUploadHandler}>
        <span className='uploadText'>
          Upload
        </span>
      </button>}
      { uploading === 1 &&  <button className="uploadingButton" disabled>
        <span className='uploadText'>
          Uploading
        </span>
      </button>}
      { uploading === 2 &&  <button className="uploadedButton" disabled>
        <span className='uploadText'>
          Uploaded!
        </span>
      </button>}
      </div>
    );

}

export default FileUploder;