import React from "react";
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import './FilterButton.scss'

export default function FilterButton(props) {
  const { expand, handlePlusClick, filterIcon, expanded, filters, filtersName, handleChangeFilters } = props
  // const [expanded, setExpanded] = useState(false)
  

  return (
    <div className={expand ? "expanded filter" : "expand filter"}>
      <div className="filter-button" onClick={handlePlusClick}>
        <div className="flterIcon">
          <div className={filterIcon} />
        </div>
        <div className="label-filter-text"> Filters </div>
      </div>
      {expanded && <div className="checkboxes">
        {filtersName.map(
          filter =>
            <div className="checkbox" key={filter}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={filters[filter]}
                    disabled={filter === 'Duplicate Keys'? true : false}
                    onChange={handleChangeFilters(filter)}
                    value={filter}
                    color="primary"
                  />
                }
                label={filter}
              />
            </div>
        )}
      </div>}
      <div style={{ width: '100%', alignSelf: 'flex-end', height: '2rem' }}></div>
    </div>
  );
}