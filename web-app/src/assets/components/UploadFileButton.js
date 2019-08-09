import React, {useState} from 'react';
import './UploadFileButton.scss';

function UploadFileButton(props) {
  const [stat, setStat] = useState(true);
  function handleChangeFocus() {
    setStat(false)
  }
  return (
     
    <>
      <button className="uploadbutton" style={props.style} onFocus={handleChangeFocus} onBlur={() => setStat(true)} onClick={() => console.log("Hey! you're gonna upload your file soon!")}>
          <img
            alt="..."
            src={require("../img/icons/common/folder_open.svg")}
            className='uploadIcon'
          />
            <ul className='uploadText'>
              Upload Docker-compose
            </ul>
      </button>
    </>
    
  
  );
}  
export default UploadFileButton;