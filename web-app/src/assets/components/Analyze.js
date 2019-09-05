import React, { Component } from 'react';
import Lottie from 'react-lottie';
import axios from 'axios';

import animationData from '../lotties/clock.json';



class Analyze extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: this.props.data,
            resault: null,
        }
        this.defaultOptions = {
            loop: true,
            autoplay: true,
            animationData: animationData,
            rendererSettings: {
                preserveAspectRatio: 'xMidYMid slice'
            }
        };
        console.log(this.state.data)
        this.apiCall();
    }
    apiCall = () => {
        axios.post('http://localhost:5000/analyzing', this.state.data, {
            mode: 'cors',
        })
            .then(res => {
                console.log(res.data)
                this.setState({ resault: res })
                // setTimeout(() => setOpen(false), 1500)
            });
    }
    render() {
        return (
            <div>
                <Lottie
                    options={this.defaultOptions}
                    height={400}
                    width={400}
                />
            </div>
        )
    }
}

export default Analyze;