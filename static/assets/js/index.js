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
    ages.forEach((box) => {
        let inputs = $(box).find('input')  
        for (i in inputs)
        {
            console.log(inputs[i].value)
        }
    });
      let body = {residence : residence_list, origine: origine_list};
      let myHeaders = new Headers();
      myHeaders.append("Content-Type","application/json"); //Important or request.get_json() returns None 

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
                let link = document.getElementById('download')
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

function add_age_range()
{
    console.log('la')
    let dumyDiv = document.createElement('div');

    let template = `
    <div class="row" style="align-items: center;justify-content: center; margin-bottom:10px;">
    <div class="col text-center d-inline-flex flex-row justify-content-around" name="age_col">
        <div><label>Min:</label><input type="number" min="13" class="age_min" max="65" value="13" /></div>
        <div><label>Max:</label><input type="number" min="13" class="age_max" max="65" value="65" /></div>
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