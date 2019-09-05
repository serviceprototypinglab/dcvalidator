import React from 'react';
import InputBase from '@material-ui/core/InputBase';
import { Link } from 'react-router-dom';

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
        <Link to='/analyzing'>
          <SearchIcon className='searchIcon' onClick={searchClicked} />
        </Link>
      </button>

    </>


  );
}
export default GithubButton;