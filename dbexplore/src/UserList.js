import React from "react";
import Profile from "./Profile";

const UserList = ({ contacts }) => {
  return (
    <div className="container">
      <div className="row">
        {contacts.map((contact) => (
          <Profile key={contact.id} names={contact.pseudos} age={contact.age} city={contact.city} avatars={contact.avatars} />
        ))}
      </div>
    </div>
  );
};

export default UserList;
