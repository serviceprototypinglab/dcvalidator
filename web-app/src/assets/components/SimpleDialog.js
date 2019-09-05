import React from 'react';
import Dialog from '@material-ui/core/Dialog';


export default function SimpleDialog(props) {
    const {
      onClose,
      open,
      component,
      onEscapeKeyDown,
    } = props;
  
    function handleClose() {
      onClose();
    }
  
    return (
      <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open} maxWidth={false} PaperProps={{style:{
        borderRadius: '1.5vh',
        padding: '3vh 3vh 0 3vh',
      }}} 
      onEscapeKeyDown={onEscapeKeyDown}
      transitionDuration={500}
      >
        {component}
      </Dialog>
    );
  }