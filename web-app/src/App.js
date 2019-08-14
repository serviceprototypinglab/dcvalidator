import React from 'react';
import GithubButton from './assets/components/GithubButton';
import UploadFileButton from './assets/components/UploadFileButton';

import './App.scss';

class App extends React.Component {
  state = {
    response: '',
    post: '',
    responseToPost: '',
  };
  
  componentDidMount() {
    this.callApi()
      .then(res => this.setState({ response: res.express }))
      .catch(err => console.log(err));
  }
  
  callApi = async () => {
    const response = await fetch('/api/hello');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    
    return body;
  };
  
  handleSubmit = async e => {
    e.preventDefault();
    const response = await fetch('/api/world', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ post: this.state.post }),
    });
    const body = await response.text();
    
    this.setState({ responseToPost: body });
  };

  render() {
    return (
      <div className="App">

        <header className="App-logo">
        {/*<img
              alt="..."
              src={require("./assets/img/brand/SPLab.svg")}
              className='SPLabLogo'
        />*/}
        Name Goes here!
        </header>

        <GithubButton />
        <UploadFileButton />
        <div>
          <p>{this.state.response}</p>
          <form onSubmit={this.handleSubmit}>
            <p>
              <strong>Post to Server:</strong>
            </p>
            <input
              type="text"
              value={this.state.post}
              onChange={e => this.setState({ post: e.target.value })}
            />
            <button type="submit">Submit</button>
          </form>
          <p>{this.state.responseToPost}</p>
        </div>
      </div>
    );
  }
}


export default App;
