import React, {useState} from 'react';
import { ReactComponent as UploadFileIcon } from '../img/icons/common/folder_open.svg';
import FileUploder from './FileUploder';
import SimpleDialog from './SimpleDialog';

import './UploadFileButton.scss';


export default function UploadFileButton(props) {
  const [open, setOpen] = useState(false);
  const {fileSelectedHandler, draged, selectedFiles, uploading, uploadPercentage, fileUploadHandler } = props;
  function handleClickOpen() {
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  };

  return (
     
    <>
      <button className="uploadFileButton" style={props.style}  onClick={handleClickOpen}>
          <UploadFileIcon className='uploadFileIcon' />
            <ul className='uploadFileText'>
              Upload Docker-compose
            </ul>
      </button>
      <SimpleDialog
        open={open}
        onClose={handleClose}
        component={
          <FileUploder
            fileSelectedHandler={fileSelectedHandler}
            draged={draged}
            selectedFiles={selectedFiles}
            uploading={uploading}
            uploadPercentage={uploadPercentage}
            fileUploadHandler={fileUploadHandler}
          />
        }
        onEscapeKeyDown={handleClose}
      />
    </>
    
  
  );
}