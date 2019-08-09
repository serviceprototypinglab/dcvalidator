import React from 'react';
import GithubButton from './assets/components/GithubButton';
import UploadFileButton from './assets/components/UploadFileButton';

import './App.scss';

function App() {
  
  return (
    <div className="App">
      
      <header className="App-logo">
      <img
            alt="..."
            src={require("./assets/img/brand/SPLab.svg")}
            className='SPLabLogo'
          />
      </header>
      
      <GithubButton />
      <UploadFileButton />
      

    </div>
  );
}


export default App;
