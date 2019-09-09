import React from 'react';
import './Resault.scss'
import { ReactComponent as LeftArrow } from '../img/icons/common/left-arrow.svg'

function Resault(props) {
    const resault = props.resault
    const downloadTxtFile = () => {
        const element = document.createElement("a");
        const file = new Blob(resault.data.logs, { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = "resault.txt";
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
    }
    return (
        <div className="resault-container">
            <div className="resault-header">Resault</div>
            <div className="paper">
                <>
                    {resault.data.logs.map(line => <span>{line}</span>)}
                </>
            </div>
            <div className="button-bar">
                <button className="resault-back-button" onClick={props.home}>
                    <LeftArrow className="left-arrow" />
                </button>
                <button className="resault-download-button" onClick={downloadTxtFile}>
                    <div className="text">download</div>
                </button>
            </div>
        </div>
    );
}

export default Resault;