import React, {useState} from 'react';
import Dialog from '@material-ui/core/Dialog';
import FileUploder from './FileUploder';
import { ReactComponent as UploadFileIcon } from '../img/icons/common/folder_open.svg';

import './UploadFileButton.scss';



function SimpleDialog(props) {
  const {
    onClose,
    open,
    fileSelectedHandler,
    draged,
    selectedFiles,
    uploading,
    uploadPercentage,
    fileUploadHandler
  } = props;

  function handleClose() {
    onClose();
  }

  return (
    <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open} maxWidth={false} PaperProps={{style:{
      borderRadius: '1.5vh',
      padding: '3vh 3vh 0 3vh',
    }}} 
    onEscapeKeyDown={handleClose}
    transitionDuration={500}
    >
      <FileUploder
        fileSelectedHandler={fileSelectedHandler}
        draged={draged}
        selectedFiles={selectedFiles}
        uploading={uploading}
        uploadPercentage={uploadPercentage}
        fileUploadHandler={fileUploadHandler}
      />
    </Dialog>
  );
}





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
        fileSelectedHandler={fileSelectedHandler}
        draged={draged}
        selectedFiles={selectedFiles}
        uploading={uploading}
        uploadPercentage={uploadPercentage}
        fileUploadHandler={fileUploadHandler}
      />
    </>
    
  
  );
}