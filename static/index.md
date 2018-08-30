# Lobster Game

## What is it?

I found this game in Year 7 when our Maths teacher, Mr Elliot, decided to play this game with us as a means of passing time towards the end of the year while hopefully instilling some intuition for probability. Unfortunately for him, variance hits hard and people felt bad. Pretty fun game though.

<blockquote class="blockquote text-right">
    <p class="mb-0">Mathematics was a mistake.</p>
    <footer class="blockquote-footer">Dr Du <cite title="Source Title">Year 12 4U Topic Enchancement VII</cite></footer>
</blockquote>

## Rules

The rules that this is based on can be found [here](http://www.suffolkmaths.co.uk/pages/Maths Projects/Games/Lobster Game/Lobster_Game_Rules.docx). There are some differences, however.

* People can work on every day of the week, including Sunday.
* Weekly costs are calculated on Sunday instead of Saturday.
* The advanced rules are in effect. This means:
    * You can buy boats for $150, selling them for half as much: $75.
        * You cannot buy boats while in debt.
    * If you are in debt come Sunday, you are charged 10% interest.
    * Running costs are modified based on how many boats you own.
* You cannot own less than 1 boat.
* Hurricanes bring everyone's boat counts down to 1.
* It's probably not worth it at this point in time to work at the hotel.

These will probably be subject to further fine tuning.

### Profit Chart

<table class="table">
    <thead>
        <tr>
            <th scope="col"></th>
            <th scope="col">Inshore</th>
            <th scope="col">Offshore</th>
        </tr>
        <tr>
            <th scope="row">Good</th>
            <td>$3</td>
            <td>$5</td>
        </tr>
        <tr>
            <th scope="row">Bad</th>
            <td>$5</td>
            <td>-$6</td>
        </tr>
    </thead>
</table>

### Button Interface

* You can join with any ID, even one is already connected. If so, you'll play as that person.
* Please don't press `Restart` unless everyone has previously agreed as it restarts the game for everyone.
* `Next Turn` will advance the turn once every ID currently connected has submitted a strategy.
* To quit the game for a player, join as that player then use the `Leave` button.
