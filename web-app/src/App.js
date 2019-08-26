import React, {useState} from 'react';
import axios from 'axios';

import GithubButton from './assets/components/GithubButton';
import UploadFileButton from './assets/components/UploadFileButton';
import FilterButton from './assets/components/FilterButton';

import './App.scss';


function App() {
  const [filterIcon, SetFilterIcon] = useState('plus icon')
  const [expand, SetExpand] = useState(false)
  const [expanded, setExpanded] = useState(false)
  const [gitURL, SetGitURL] = useState('');
  const [selectedFiles, SetSelectedFiles] = useState([])
  const [uploadPercentage,SetUploadPercentage] = useState(0)
  const [uploading,SetUploading] = useState(0) // 0: No    1: uploading    2: finished
  const [draged,SetDraged] = useState(false)
  const filters = ['Duplicate service name','Duplicate container name','Duplicate image','Duplicate port']
  
  const labelSend = () => {
    var data = new FormData();
    data.append('labels', filters)
    axios.post('http://localhost:5000/filters', data, { 
      mode: 'cors',
    })
      .then(res => {
        console.log(res);
      });
  }


  const searchClicked = () => {
    console.log("It's working!")
    axios.get('http://localhost:5000/url', {
      params: {
        url: gitURL
      }
    }).then(res => {
      console.log(res.data)
    })
    labelSend()
  }

  const fileUploadHandler = () => {
    var data = new FormData();
    selectedFiles.map(file => data.append('file[]', file))
    SetUploading(1)
    axios.post('http://localhost:5000/upload', data, { 
      mode: 'cors',
      onUploadProgress: ProgressEvent => {
        var uploadProgress = Math.round(ProgressEvent.loaded / ProgressEvent.total * 100)
        SetUploadPercentage(uploadProgress)
      }
    })
      .then(res => {
        SetUploading(2)
        console.log(res);
      });
  }


  const urlInputChange = (e) => {
    SetGitURL(e.target.value)
    console.log(e.target.value)
  }
  

  const fileSelectedHandler = event => {
    let files =  selectedFiles
    event.map(file => {
      if (!(file in files)) {
        files.push(file)
      }
      return null
    })

    SetSelectedFiles(files)
    SetDraged(true)
  }
  
  const handlePlusClick = () => {
    if (filterIcon === 'plus icon') {
      SetFilterIcon('remove icon')
      SetExpand(true)
      setTimeout(() => setExpanded(true),200);
    }else {
      SetFilterIcon('plus icon')
      SetExpand(false)
      setExpanded(false)
    }
  }
    return (
      <div className="App">

        <header className="App-logo">
        
        Docker Compose Validator!
        </header>
        <span className="boddy">
        <GithubButton
          searchClicked={searchClicked}
          urlInputChange={urlInputChange}
          gitURL={gitURL}
        />
        <span>
          <UploadFileButton
            fileSelectedHandler={fileSelectedHandler}
            draged={draged}
            selectedFiles={selectedFiles}
            uploading={uploading}
            uploadPercentage={uploadPercentage}
            fileUploadHandler={fileUploadHandler}
          />
          <FilterButton
            expand={expand}
            handlePlusClick={handlePlusClick}
            filterIcon={filterIcon}
            expanded={expanded}
            filters={filters}
          />
        </span>
        </span>
        <footer className="App-footer">
          <img
              alt="..."
              src={require("./assets/img/brand/SPLab.svg")}
              className='logo'
          />
          <img
              alt="..."
              src={require("./assets/img/brand/logos_ZHAW.svg")}
              className='logo'
          />
        </footer>
      </div>
    );

}


export default App;
