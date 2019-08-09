import React, {useState} from 'react';
import './GithubButton.scss';
import InputBase from '@material-ui/core/InputBase';

function GithubButton(props) {
  const [stat, setStat] = useState(true);
  function handleChangeFocus() {
    setStat(false)
  }
  
  return (
     
    <>
      <button className="button" style={props.style} onFocus={handleChangeFocus} onBlur={() => setStat(true)}>

        <> 
          <img
            alt="..."
            src={require("../img/icons/common/github.svg")}
            className='githubIcon'
          />
            <ul className='label'>
              Github Repository
            </ul>
        </>
        <InputBase className='textInput' placeholder={'YourGithubLink e.g: https://github.com/alidaghighi/docker-compose-file-validator'} />
      </button>
    </>
    
  
  );
}  
export default GithubButton;