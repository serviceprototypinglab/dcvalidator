import React, { useState } from "react";
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import './FilterButton.scss'

export default function FilterButton(props) {
    const {expand, handlePlusClick, filterIcon, expanded, filters} = props
    const [state, setState] = useState({
        checkedB: true,
      });
    // const [expanded, setExpanded] = useState(false)
      const handleChange = name => event => {
        setState({ ...state, [name]: event.target.checked });
      };

    return (
        <div className={expand ? "expanded filter" : "expand filter"} onBlur={handlePlusClick}>
          <div className="filter-button" onClick={handlePlusClick}>
            <div className="flterIcon">
              <div className={filterIcon} />
            </div>
            <div className="label-filter-text"> Filters </div>
          </div>
          {expanded && <div className="checkboxes">
            {filters.map(
                filter =>
                <div className="checkbox">
                <FormControlLabel
                control={
                    <Checkbox
                    checked={state.checkedB}
                    onChange={handleChange('checkedB')}
                    value="checkedB"
                    color="primary"
                />
                }
                label={filter}
                key={filter}
                />
                </div>
            )}
        </div>}
        <div style={{width:'100%', alignSelf:'flex-end', height:'2rem'}}></div>
        </div>
    );
}