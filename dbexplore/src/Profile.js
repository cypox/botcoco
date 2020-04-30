import React from "react";
import "./Profile.css";

function Profile(props) {
  return (
    <div class="col-sm-6 col-md-4 col-lg-3 mt-4">
      <div class="card">
        <img class="card-img-top" src={"" + props.avatar}></img>
        <div class="card-block">
          <h4 class="card-title mt-3">{props.name}</h4>
          <div class="meta">
            <h5>
              {props.city}, {props.age} ans
            </h5>
          </div>
        </div>
        <div class="card-footer">
          <div class="icon pull-right"></div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
