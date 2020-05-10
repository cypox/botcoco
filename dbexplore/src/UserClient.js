import React, { Component } from "react";
import UserList from "./UserList";

// THIS IS NOT USED NOW

class UserClient extends Component {
  state = {
    contacts: []
  }

  componentDidMount() {
    fetch('http://jsonplaceholder.typicode.com/users')
    .then(res => res.json())
    .then((data) => {
      this.setState({contacts: data})
    })
    .catch(console.log)
  }

  render() {
    return (<UserList contacts = {this.state.contacts}/>)
  }
}

export default UserClient;
