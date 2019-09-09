import React, { Component } from 'react';
import Lottie from 'react-lottie';

import animationData from '../lotties/clock.json';



class Analyze extends Component {
    constructor(props) {
        super(props);
        this.defaultOptions = {
            loop: true,
            autoplay: true,
            animationData: animationData,
            rendererSettings: {
                preserveAspectRatio: 'xMidYMid slice'
            }
        };
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