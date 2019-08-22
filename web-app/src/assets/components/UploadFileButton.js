import React, {useState} from 'react';
import Dialog from '@material-ui/core/Dialog';
import FileUploder from './FileUploder';
import { ReactComponent as UploadFileIcon } from '../img/icons/common/folder_open.svg';

import './UploadFileButton.scss';



function SimpleDialog(props) {
  const { onClose, open } = props;

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
      <FileUploder />
    </Dialog>
  );
}





export default function UploadFileButton(props) {
  const [open, setOpen] = useState(false);
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
      <SimpleDialog open={open} onClose={handleClose} />
    </>
    
  
  );
}