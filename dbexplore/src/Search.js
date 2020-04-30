import React from "react";
import axios from "axios";
import "./Search.css";
import UserList from "./UserList";

class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      results: {},
      loading: false,
      message: "",
    };
    this.cancel = "";
  }

  getPagesCount = (total, denominator) => {
    const divisible = total % denominator === 0;
    const valueToBeAdded = divisible ? 0 : 1;
    return Math.floor(total / denominator) + valueToBeAdded;
  };

  fetchSearchResults = (updatedPageNo = "", query) => {
    const pageNumber = updatedPageNo ? `&page=${updatedPageNo}` : "";
    const searchUrl = `http://127.0.0.1:8080/query/${query}`;
    if (this.cancel) {
      // Cancel the previous request before making a new request
      this.cancel.cancel();
    }
    // Create a new CancelToken
    this.cancel = axios.CancelToken.source();
    axios
      .get(searchUrl, {
        cancelToken: this.cancel.token,
      })
      .then((res) => {
        const resultNotFoundMsg = !res.data.users.length
          ? "There are no more search results. Please try a new search."
          : "";
        this.setState({
          results: res.data.users,
          message: resultNotFoundMsg,
          loading: false,
        });
      })
      .catch((error) => {
        if (axios.isCancel(error) || error) {
          this.setState({
            loading: false,
            message: "Failed to fetch results.Please check network",
          });
        }
      });
  };

  renderSearchResults_old = () => {
    const { results } = this.state;
    if (Object.keys(results).length && results.length) {
      return (
        <div className="results-container">
          {results.map((result) => {
            return (
              <a
                key={result.id}
                href={result.id}
                className="result-items"
              >
                <h6 className="image-username">{result.pseudos[0].name}</h6>
                <div className="image-wrapper">
                  <img
                    className="image"
                    src={'http://127.0.0.1:8080/'+result.id+'-000.jpg'}
                    alt={result.id}
                  />
                </div>
              </a>
            );
          })}
        </div>
      );
    }
  };

  renderSearchResults = () => {
    const { results } = this.state;
    if (Object.keys(results).length && results.length) {
      return (
        <UserList contacts={results}/>
      );
    }
  };

  render() {
    const { query } = this.state;
    const {message, loading} = this.state;
    return (
      <div className="container">
        {/*Heading*/}
        <h2 className="heading">DB Explorer</h2>
        {/*Search Input*/}
        <label className="search-label" htmlFor="search-input">
          <input
            type="text"
            value={query}
            id="search-input"
            placeholder="Search..."
            onChange={this.handleOnInputChange}
          />
          <i className="fa fa-search search-icon" />
        </label>
        {/*Result*/}
        {this.renderSearchResults()}
        {/*Error Message*/}
        {message && <p className="message">{message}</p>}
      </div>
    );
  }

  handleOnInputChange = (event) => {
    const query = event.target.value;
    if (!query || query.length < 3) {
      this.setState({ query, results: {}, message: "" });
    } else {
      this.setState({ query, loading: true, message: "" }, () => {
        this.fetchSearchResults(1, query);
      });
    }
  };
}

export default Search;
