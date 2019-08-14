import React, {useState} from 'react';
import Dialog from '@material-ui/core/Dialog';
import FileUploder from './FileUploder';
import './UploadFileButton.scss';


const emails = ['username@gmail.com', 'user02@gmail.com'];


function SimpleDialog(props) {
  const { onClose, selectedValue, open } = props;

  function handleClose() {
    onClose(selectedValue);
  }

  return (
    <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open}>
      <FileUploder />
    </Dialog>
  );
}





export default function UploadFileButton(props) {
  const [stat, setStat] = useState(true);
  const [open, setOpen] = React.useState(false);
  const [selectedValue, setSelectedValue] = useState(emails[1]);
  function handleClickOpen() {
    setOpen(true);
  }

  const handleClose = value => {
    setOpen(false);
    setSelectedValue(value);
  };


  function handleChangeFocus() {
    setStat(false)
  }

  return (
     
    <>
      <button className="uploadbutton" style={props.style} onFocus={handleChangeFocus} onBlur={() => setStat(true)} onClick={handleClickOpen}>
          <img
            alt="..."
            src={require("../img/icons/common/folder_open.svg")}
            className='uploadIcon'
          />
            <ul className='uploadText'>
              Upload Docker-compose
            </ul>
      </button>
      <SimpleDialog selectedValue={selectedValue} open={open} onClose={handleClose} />
    </>
    
  
  );
}