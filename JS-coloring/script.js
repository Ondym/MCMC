let nodes;
let nodeSize;
let totalBlobs;
let lastBlobNodes;
let n;
let colorify = false;
let HUEstep;

let maxBlobSize = 0;
let lastStateEnergy = 0; 

let info;
let totalInfo;
let totalStats = {
    rounds: 0,
    blobCount: 0,
    nodesPerBlob: 0,
    totalEnergy: 0
}

let k_B = 1; // setting the Boltzmann constant to 1
let T = 20;  // temperature  of the box (in K) 

let doChanges = true;

Object.defineProperty(Array.prototype, 'includesVector', {
    value: function(_v) { 
        for (let i = 0; i < this.length; i++) {
            if (this[i].x == _v.x && this[i].y == _v.y) {
                return true;
            }
        }

        return false;
     }
});

function setup() {
    // pixelDensity(1);
    createCanvas(600, 600);

    info = document.getElementById("tit") 
    totalInfo = document.getElementById("avg-tit");
    
    // RANDOM SCATTERING OF POINT IN THE BIGINNING 50/50
    /*nodes = new Array;
        let size = 256;
        n = 0;
        for (let i = 0; i < size; i++) {
            nodes.push(new Array);
            for (let j = 0; j < size; j++) {
                nodes[i].push(genValue(0.5));
                if (nodes[i][j]) n++;
            }
        }*/

    nodes = GRID;
        
    nodeSize = width / nodes.length;
    // HUEstep = 150 / (maxBlobSize ** 1/2);

    lastStateEnergy = countDifferences();
    lastBlobNodes = new Array;
    
    totalBlobs = separateBlobs();
    HUEstep = 200 / (maxBlobSize ** 1/2);
}

function draw() {
    noStroke();
    
    // CHANGING
    
    // let changePos = simpleVector(floor(random(nodes.length)), floor(random(nodes.length)));
    // nodes[changePos.x][changePos.y] = (nodes[changePos.x][changePos.y] + 1) % 2;
    
    // let changedPointEnergy = calcNodeEnergy(changePos.x, changePos.y);
    
    // deltaEnergy = 4 - 2*changedPointEnergy;
    // // console.log(changePos, deltaEnergy);
    // let alpha = acceptanceRatio(deltaEnergy);

    
    // if (!random() < alpha) {
    //     nodes[changePos.x][changePos.y] = (nodes[changePos.x][changePos.y] + 1) % 2;
    // }

    // // DATA CHARACTERISTICS

    
    // let avgNodesPerBlob = floor(n / totalBlobs.length * 10**4) / 10**4;
    
    // info.innerText = "Počet (černých) bodů: " + n + "\nEnergie: " + lastStateEnergy + "\nAVG # bodů v blobu: " + avgNodesPerBlob;
    
    // totalStats.nodesPerBlob += avgNodesPerBlob; 
    // totalStats.blobCount += totalBlobs.length;
    // totalStats.totalEnergy += countDifferences();
    // totalStats.rounds++;
    

    // totalInfo.innerText = 
    // "Počet kol: " + totalStats.rounds + 
    // "\nAVG počet blobů: " + floor(totalStats.blobCount/totalStats.rounds * 10**4) / 10**4 + 
    // "\nAVG # bodů v blobu: " + floor(totalStats.nodesPerBlob/totalStats.rounds * 10**4) / 10**4 +
    // "\nAVG energie: " + floor(totalStats.totalEnergy/totalStats.rounds * 10**4) / 10**4;

    
    //      VISUALS
    noStroke();
    background(255);
    fill(0);
    
    if (colorify) {
        colorMode(HSB);
        for (let i = 0; i < totalBlobs.length; i++) {
            for (let j = 0; j < totalBlobs[i].length; j++) {
                fill(totalBlobs[i].length ** 1/2 * HUEstep, 90, 90);
                rect(totalBlobs[i][j].x * nodeSize, totalBlobs[i][j].y * nodeSize, nodeSize*1.2, nodeSize*1.2);
            }
        }
        colorMode(RGB);

    } else {
        for (let i = 0; i < nodes.length; i++) {
            for (let j = 0; j < nodes[0].length; j++) {
                if (nodes[i][j]) {
                    rect(i*nodeSize, j*nodeSize, nodeSize*1.1, nodeSize*1.1);
                }
            }
        }
    }
    
    if (colorify) fill(10);
    else          fill(215, 120, 18);
    
    for (let i = 0; i < lastBlobNodes.length; i++) {
        rect((lastBlobNodes[i].x + .25) * nodeSize, (lastBlobNodes[i].y + .25) * nodeSize, nodeSize/2, nodeSize/2);
    }
}

function mouseClicked() {
    if (constrain(mouseX, 0, width) != mouseX || constrain(mouseY, 0, height) != mouseY) {
        return;
    }
    lastBlobNodes = getBlob(floor(mouseX/nodeSize), floor(mouseY/nodeSize));
}

function keyPressed() {
    if (keyCode == ENTER) {
        colorify = !colorify;
    }
    if (keyCode == 32) {
        doChanges = !doChanges;
        if (doChanges) {
            fill(255);
            rect(0, 0, width, height);
            fill(0);
            textSize(28);
            text("Pro urychlení není podporován obraz při generování. \n     Stisknutím [MEZERY] generování zastavíte. ", 20,  300)
        }
    }
}

function genValue(_p) {
    // _p is the probability of getting 1
    return random() < _p ? 1 : 0
}

function getBlob(_x, _y) {
    if (!nodes[_x][_y]) return new Array;
    let opened = [simpleVector(_x, _y)];
    let blobNodes = [].concat(opened);

    let m = 0;
    while (opened.length > 0) {
        m++; // insurance
        let newOpened = new Array;

        for (let i = 0; i < opened.length; i++) {
            for (let X = -1; X < 2; X++) {
                for (let Y = -1; Y < 2; Y++) {
                    if (abs(X) + abs(Y) == 1) {
                        let nextVector = simpleVector(
                            (opened[i].x + X + nodes.length) % nodes.length, // adding nodes.length to wrap -1 to the other side
                            (opened[i].y + Y + nodes.length) % nodes.length
                        );
                        if (!blobNodes.includesVector(nextVector) && nodes[nextVector.x][nextVector.y]) {
                            newOpened.push(nextVector);
                            blobNodes.push(nextVector);
                        }
                    }
                }
            }
        }

        opened = newOpened;
    }

    return blobNodes;
}

function simpleVector(_x, _y) {
    return {x: _x, y: _y};
}

function separateBlobs() {
    let nodesRegistered = [];
    maxBlobSize = 0;
    
    let retBlobs = new Array;
    for (let i = 0; i < nodes.length; i++) {
        for (let j = 0; j < nodes.length; j++) {
            if (!nodesRegistered.includesVector(simpleVector(i, j))) {
                let blob = getBlob(i, j);
                if (blob.length > 0) {
                    if (maxBlobSize < blob.length) {
                        maxBlobSize = blob.length;
                    }
                    nodesRegistered = nodesRegistered.concat(blob);
                    retBlobs.push(blob);
                }
            }
        }
    }

    return retBlobs;
}

function countDifferences() {
    let energy = 0;

    for (let i = 0; i < nodes.length; i++) {
        for (let j = 0; j < nodes[i].length; j++) {
            for (let X = -1; X < 2; X++) {
                for (let Y = -1; Y < 2; Y++) {
                    if (abs(X) + abs(Y) == 1) {
                        let neighbour = simpleVector(
                            (i + X + nodes.length)    % nodes.length, // adding nodes.length to wrap -1 to the other side
                            (j + Y + nodes[i].length) % nodes.length
                        );

                        if (nodes[i][j] != nodes[neighbour.x][neighbour.y]) {
                            energy ++;
                        }
                    }
                }
            }
        }
    }

    return energy / 2;
}

function calcNodeEnergy(_x, _y) {
    let energy = 0;
    
    for (let X = -1; X < 2; X++) {
        for (let Y = -1; Y < 2; Y++) {
            if (abs(X) + abs(Y) == 1) {
                let neighbour = simpleVector(
                    (_x + X + nodes.length)    % nodes.length, // adding nodes.length to wrap -1 to the other side
                    (_y + Y + nodes[_x].length) % nodes.length
                );

                if (nodes[_x][_y] != nodes[neighbour.x][neighbour.y]) {
                    energy ++;
                }
            }
        }
    }

    return energy;
}

function acceptanceRatio(_delta) {
    return min(1, exp(-(_delta/(k_B*T))));
}