import React, { useMemo, useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import LinearProgress from '@material-ui/core/LinearProgress';
import Lottie from 'react-lottie';

import { ReactComponent as YmlIcon } from '../img/icons/common/yml.svg';
// import { ReactComponent as DeleteIcon } from '../img/icons/common/delete.svg';
import loadingAnimationData from '../lotties/loader.json';
import doneAnimationData from '../lotties/done.json';



import './FileUploader.scss';

const baseStyle = {
  // flex: 1,
  width: '64vh',
  height: '26vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 5,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  outline: 'none',
  transition: 'border .24s ease-in-out',
  cursor: 'pointer',
};

const activeStyle = {
  borderColor: '#2196f3'
};

const acceptStyle = {
  borderColor: '#00e676',
  backgroundColor: 'rgba(64, 119, 192, 0.025)',
};

const rejectStyle = {
  borderColor: '#ff1744',
  backgroundColor: 'rgba(192, 64, 64, 0.068)',
  cursor: 'not-allowed',
};

function StyledDropzone(props) {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,

  } = useDropzone({
    onDrop: props.onDrop,
    accept: 'application/x-yaml, application/x-yaml',
    multiple: true,
  });

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? activeStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }),
    [isDragActive, isDragReject, isDragAccept]);

  return (
    <div className="container">
      <div {...getRootProps({ style })}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop some files here, or click to select files</p>
      </div>
    </div>
  );
}



function FileUploder(props) {
  const [disabled, setDisabled] = useState(false)
  const {
    fileSelectedHandler,
    draged,
    selectedFiles,
    uploading,
    uploadPercentage,
    fileUploadHandler,
  } = props;
  useEffect(() => {
    if (selectedFiles.length <= 0) {
      setDisabled(true)
    }
    else if (uploading !== 1 || uploading !== 0) {
      setDisabled(false)
    }
    return () => {
      if (selectedFiles) {
        setDisabled(true)
      }
      else if (uploading !== 1 || uploading !== 0) {
        setDisabled(false)
      }
    }
  }, [selectedFiles, uploading, props])

  const defaultOptions = {
    loop: uploading === 2 ? false : true,
    autoplay: true,
    animationData: uploading === 2 ? doneAnimationData : loadingAnimationData,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice'
    }
  };

  return (
    <div className="uploadDialog">
      <StyledDropzone onDrop={fileSelectedHandler} draged={draged} className="dropzone" />
      <span style={{ display: 'flex', justifyContent: 'flex-start', flexDirection: 'column', alignSelf: 'flex-start', width: '100%' }}>

        {selectedFiles &&

          selectedFiles.map(file => <div key={file.path} style={{ marginTop: '25px', alignItems: 'center', flexDirection: 'row', display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ display: 'flex', alignItems: 'center', flexDirection: 'row' }}>
              <YmlIcon className='ymlIcon' />
              <span className='fileName'>
                {file.path}
              </span>
              {/* <DeleteIcon className="DeleteIcon" /> */}
            </span>
          </div>)
        }
      </span>
      <span style={{ width: '100%', marginTop: '25px' }}>
        {uploading !== 0 && <LinearProgress variant="determinate" value={uploadPercentage} />}
      </span>

      <button className={disabled ? "disabledUploadButton"
        : uploading === 0 ? "uploadButton"
          : uploading === 1 ? "uploadingButton"
            : uploading === 2 ? "uploadedButton"
              : uploading === 3 ? "analysButton": "uploadedButton"}
        onClick={fileUploadHandler}
        disabled={disabled}
      >
        <span className='uploadText'>
          {uploading === 0 && <div>
            upload
          </div>}
          {uploading === 1 && <Lottie
            options={defaultOptions}
            height={90}
            width={90}
            style={{ margin: '-30px auto' }}
          />}
          {uploading === 2 && <Lottie
            options={defaultOptions}
            height={157}
            width={157}
            style={{ margin: '-60px' }}
          />
          }
          {uploading === 3 &&
            <div
              style={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'center',
                alignItems: 'center'
              }}
            >
              <span>
                Analys
              </span>
            </div>
          }
        </span>
      </button>
    </div>
  );

}

export default FileUploder;