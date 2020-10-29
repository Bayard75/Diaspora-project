function generate()
{
    let residence_checked = document.querySelectorAll('input[name=residence]:checked');
    let origine_checked = document.querySelectorAll('input[name=origine]:checked');

    let residence_list = []
    residence_checked.forEach((box) => {
        let name = box.getAttribute('data')
       residence_list.push({"id":box.id, "name":name})
      });
    
    let origine_list = []
    origine_checked.forEach((box) => {
        let name = box.getAttribute('data')
        let short_name = box.getAttribute('short-name')

        origine_list.push({"id":box.id, "name":name, "short_name": short_name})
       });
    
    let ages = document.getElementsByName("age_col")
    console.log(ages.length)
    let age_ranges = []
    ages.forEach((box) => {
        let inputs = $(box).find('input')  
        let age_list = []
        for (i in inputs)
        {
            age_list.push(inputs[i].value)
        }
        age_ranges.push(age_list.slice(0,2))
    });
      let body = {residence : residence_list, origine: origine_list, age_ranges: age_ranges};
      let myHeaders = new Headers();
      myHeaders.append("Content-Type","application/json"); //Important or request.get_json() returns None 
      let loading = document.getElementById('loading')
      loading.style.display = 'block'  
      fetch('/home', {
              // Specify the method
              method: 'POST',
              // A JSON payload
              body: JSON.stringify(body),
              headers: myHeaders
            })
            .then(function (response) 
            { 
                return response.json();

            })
            .then(function (data)
            {

                let path = data['path']
                loading.style.display = 'none'
                let link = document.getElementById('col_download')
                link.style.display = "block";  
                link.setAttribute('href', path)  
            })

}

function checkAll(card)
{
    let boxes= document.querySelectorAll(`input[name=${card}]`);
    document.getElementById('uncheckall').checked = false;
    boxes.forEach((box) => {
        box.checked = true;
    });
}
function uncheckAll(card)
{
    let boxes= document.querySelectorAll(`input[name=${card}]`);
    document.getElementById('checkall').checked = false;

    boxes.forEach((box) => {
        box.checked = false;
    });
}

function remove_age_range()
{
    let age_col = document.getElementsByName('age_body')[0]
    age_col.lastChild.remove()
}
function add_age_range()
{
    console.log('la')
    let dumyDiv = document.createElement('div');

    let template = `
    <div class="row" style="align-items: center;justify-content: center; margin-bottom:10px;">
    <div class="col text-center d-inline-flex flex-row justify-content-around" name="age_col">
        <label>Min:</label><input type="number" min="13" class="age_min" max="65" value="13" onchange ="checkInputMin(this)"/>
        <label>Max:</label><input type="number" min="13" class="age_max" max="65" value="65" onchange="checkInputMax(this)" />
    </div>
</div>    `
    let age_col = document.getElementsByName('age_body')[0]
    dumyDiv.innerHTML = template
    age_col.appendChild(dumyDiv)
}

function checkInputMin(element)
{
    let next_sibling = element.nextSibling.nextSibling.nextSibling;
    let max_value = next_sibling.value;
    if (element.value > max_value)
    {
        element.value = max_value;
    }
    if (element.value > 65)
    {
        element.value = 65;
    }
    if (element.value < 13)
    {
        element.value = 13;
    }
}

function checkInputMax(element)
{
    let previous_sibling = element.previousSibling.previousSibling.previousSibling;
    let min_value = previous_sibling.value;
    if (element.value < min_value)
    {
        element.value = min_value;
    }
    if (element.value > 65)
    {
        element.value = 65;
    }
    if (element.value < 13)
    {
        element.value = 13;
    }
}

function allNoneCheck(element)
{
    let checkboxAll = document.getElementById('checkall')
    let checkboxNone = document.getElementById('uncheckall')
    if (element.checked == true)
    {
        if (checkboxNone.checked == true)
        {
            checkboxNone.checked = false
        }
    }
    if (element.checked == false)
    {
        if (checkboxAll.checked == true)
        {
            checkboxAll.checked = false
        }
    }
}