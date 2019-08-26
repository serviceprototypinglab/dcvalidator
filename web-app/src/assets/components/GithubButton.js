import React from 'react';
import InputBase from '@material-ui/core/InputBase';

import { ReactComponent as SearchIcon } from '../img/icons/common/analytics.svg';
import { ReactComponent as GithubIcon } from '../img/icons/common/github.svg';

import './GithubButton.scss';

function GithubButton(props) {
  return (
     
    <>
      <button className="githubButton" style={props.style} >

        <> 
          <GithubIcon className='githubIcon' />
            <ul className='label'>
              Github Repository
            </ul>
        </>
        <InputBase className='textInput' placeholder={'YourGithubLink e.g: https://github.com/alidaghighi/docker-compose-file-validator'} value={props.gitURL} onChange={props.urlInputChange} />
          <SearchIcon className='searchIcon' onClick={props.searchClicked}/>
      </button>
    </>
    
  
  );
}  
export default GithubButton;