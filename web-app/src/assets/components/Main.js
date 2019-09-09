import React, { useState, useEffect } from 'react';
import axios from 'axios';


// import lottie from "lottie-web";

import GithubButton from './GithubButton';
import UploadFileButton from './UploadFileButton';
import FilterButton from './FilterButton';
// import SimpleDialog from './SimpleDialog';

import './Main.scss';

function Main(props) {
  // Initials
  // const initialFilters = {'Duplicate service name':true, 'Duplicate container name':true, 'Duplicate image':true, 'Duplicate port':true} 
  const { initialFilters, setData } = props
  const filtersName = Object.keys(initialFilters)
  const data = new FormData();

  // States
  const [filterIcon, SetFilterIcon] = useState('plus icon')
  const [expand, SetExpand] = useState(false)
  const [expanded, setExpanded] = useState(false)
  const [gitURL, SetGitURL] = useState('');
  const [selectedFiles, SetSelectedFiles] = useState([])
  const [uploadPercentage, SetUploadPercentage] = useState(0)
  const [uploading, SetUploading] = useState(0) // 0: No    1: uploading    2: finished
  const [draged, SetDraged] = useState(false)
  // const [open, setOpen] = useState(false);
  const [filters, setFilters] = useState(initialFilters);
  useEffect(() => {
      var snedfilters = []
      filtersName.map(filter => filters[filter] ? snedfilters.push(filter) : null)
      data.append('labels[]', snedfilters.toString())
      selectedFiles.map(file => data.append('file[]', file))
      // data.append('file[]', selectedFiles)
      data.append('URL', gitURL)
  })

  const apiCall = () => {
    setData(data)
  }

  const searchClicked = () => {
    console.log("It's working!")
    apiCall()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      searchClicked()
    }
  }

  const fileUploadHandler = () => {
    if (uploading !== 3) {


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
          console.log(res.data);
          setTimeout(() => SetUploading(3), 2000)
        });
    } else if(uploading === 3 || uploading === 0) {
      apiCall()
    }
  }


  const urlInputChange = (e) => {
    SetGitURL(e.target.value)
  }


  const fileSelectedHandler = event => {
    let files = selectedFiles
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
      setTimeout(() => setExpanded(true), 200);
    } else {
      SetFilterIcon('plus icon')
      SetExpand(false)
      setExpanded(false)
    }
  }

  // const handleClose = () => {
  //   setOpen(false);
  // };

  const handleChangeFilters = name => event => {
    setFilters(prevState => { return { ...prevState, [name]: event.target.checked } })

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
          handleKeyDown={handleKeyDown}
          placeholder={'YourGithubLink e.g: https://github.com/alidaghighi/docker-compose-file-validator'}
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
            handleChangeFilters={handleChangeFilters}
            filtersName={filtersName}
          />
        </span>
      </span>
      {/* <footer className="App-footer">
        <img
          alt="..."
          src={require("../img/brand/SPLab.svg")}
          className='logo'
        />
        <img
          alt="..."
          src={require("../img/brand/logos_ZHAW.svg")}
          className='logo'
        />
      </footer> */}
      {/* <SimpleDialog
          open={open}
          onClose={handleClose}
          component={ */}
      {/* <Route path="/analysing" component={loadingComponent} /> */}

      {/* }
        /> */}
    </div>
  );

}


export default Main;
