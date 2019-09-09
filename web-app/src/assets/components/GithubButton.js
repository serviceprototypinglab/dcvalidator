import React from 'react';
import InputBase from '@material-ui/core/InputBase';

import { ReactComponent as SearchIcon } from '../img/icons/common/analytics.svg';
import { ReactComponent as GithubIcon } from '../img/icons/common/github.svg';

import './GithubButton.scss';

function GithubButton(props) {
  const { style, searchClicked, gitURL, urlInputChange, handleKeyDown, placeholder } = props

  return (

    <>

      <button className="githubButton" style={style} >

        <>
          <GithubIcon className='githubIcon' />
          <ul className='label'>
            Github Repository
            </ul>
        </>
        <InputBase className='textInput' placeholder={placeholder} value={gitURL} onChange={urlInputChange} onKeyDown={handleKeyDown} />
          <SearchIcon className='searchIcon' onClick={searchClicked} />
      </button>

    </>


  );
}
export default GithubButton;