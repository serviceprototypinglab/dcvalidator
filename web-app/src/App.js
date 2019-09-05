import React, {Component, useEffect, useState} from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';

import Main from './assets/components/Main';
import Analyze from './assets/components/Analyze';
import PageNotFound from './assets/components/PageNotFound';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = { 
            initialFilters: {},
            data: {}
         };
         axios.get('http://localhost:5000/getlabels').then(res => {
            var tmpinitialFilters = this.state.initialFilters
            res.data.labels.map(label => {
                tmpinitialFilters[label] = true
            })
            this.setState({initialFilters: tmpinitialFilters}) 
        })

    }
    setData = (data) => {
        this.setState(data)
    }
    render() {
        const {initialFilters} = this.state
        return (
            <Router>
            <Switch>
                <Route path="/" exact component={() => (
                    <Main initialFilters={initialFilters} setData={this.setData} />
                )} />
                <Route path="/analyzing" component={() => (
                    <Analyze data={this.state.data}/>
                )} />
                <Route component={() => (
                    <PageNotFound />
                )} />
            </Switch>
        </Router>
        );
    }
}

export default App;