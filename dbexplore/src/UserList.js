import React from "react";
import Profile from "./Profile";
import Button from "react-bootstrap/Button";

const UserList = ({ contacts }) => {
  return (
    <div class="container">
      <div class="row">
        {contacts.map((contact) => (
          <Profile
            name={contact.name}
            age={contact.email}
            city={contact.address.city}
          />
        ))}
      </div>
    </div>
  )
};

export default UserList;
