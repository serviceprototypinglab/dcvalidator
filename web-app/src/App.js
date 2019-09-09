import React, { Component } from 'react';

import axios from 'axios';

import Main from './assets/components/Main';
import Analyze from './assets/components/Analyze';
import Resault from './assets/components/Resault';

import './App.scss'

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            initialFilters: {},
            resault: null,
            page: 'home',
        };
        this.data = {}
        axios.get('http://localhost:5000/getlabels').then(res => {
            var tmpinitialFilters = this.state.initialFilters
            res.data.labels.map(label => tmpinitialFilters[label] = true)
            this.setState({ initialFilters: tmpinitialFilters })
        })

    }
    setData = (data) => {
        this.data = data
        this.setState({ page: 'analyzing' }, () => this.apiCall())
    }
    apiCall = () => {
        axios.post('http://localhost:5000/analyzing', this.data, {
            mode: 'cors',
        })
            .then(res => {
                console.log(res.data)
                this.setState({ resault: res, page: 'resault' })
                // setTimeout(() => setOpen(false), 1500)
            });
    }
    backHome = () => {
        this.setState({ page: 'home' })
    }
    render() {
        const { initialFilters, page, resault } = this.state
        return (
            <div className="container">
                {page === 'home' && <Main initialFilters={initialFilters} setData={this.setData} />}
                {page === 'analyzing' && <Analyze />}
                {page === 'resault' && <Resault resault={resault} home={this.backHome} />}
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
}

export default App;