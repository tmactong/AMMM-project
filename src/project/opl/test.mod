/*********************************************
 * OPL 22.1.1.0 Model
 * Author: tmactong
 * Creation Date: Apr 3, 2025 at 11:51:05 AM
 *********************************************/


int MemberNo=5;
//{int} MemberSet = asSet(1..MemberNo);

//int MemberChains[1..6][1..6];
int Count;

execute CalculateNoRepetitionSequenceCount {
  
  function CalculateCombinationCount(allMemberCount, chosenMemberCount) {
    var CombinationCount = 1;
    for (var i=allMemberCount;i>allMemberCount-chosenMemberCount;i--) {
      CombinationCount = CombinationCount*i
    }
    for (var j=1;j<=chosenMemberCount;j++) {
      CombinationCount = CombinationCount / j;
    }
    return CombinationCount;
  }

  function CalculatePermutationCount(memberCount) {
    var permutationCount = 1;
    for (var i=memberCount;i>=1;i--) {
      permutationCount = permutationCount * i; 
    }
    return permutationCount;
  }
  
  function CalculateSequenceCount(memberCount) {
    var totalSequenceCount = 0;
    for (var i=0;i<memberCount-2;i++) {
      var sequenceCount = 1;
      // moving member count = i
      // availablely moving count = memberCount -3
      // residual member count = memberCount - 2 - i;
      for (var j=1;j<=i;j++) {
        sequenceCount = sequenceCount * (memberCount - 2 -j);
      }
      var permutationCount = CalculatePermutationCount(memberCount-2-i);
      sequenceCount = sequenceCount * permutationCount;
      totalSequenceCount += sequenceCount; 
    }
    return totalSequenceCount;
  }
  
  //Count = CalculateSequenceCount(8);
  //writeln('count: ', Count);
  
  //var count = CalculateCombinationCount(5,3);
  //writeln('count: ', count);
  
  var totalChainCount = 0;
  for (var i=3;i<=MemberNo;i++) {
    var combinationCount = CalculateCombinationCount(MemberNo, i);
    var sequenceCount = CalculateSequenceCount(i);
    totalChainCount += combinationCount * sequenceCount;
  }
  writeln('total chain count: ', totalChainCount);
}

/*
execute populateMemberChains {
  for (var i=1;i<=6;i++) {
    for (var j=1;j<=3;j++) {
      MemberChains[i][j] = i;
    }
  }
  for (var i=1;i<=6;i++) {
    writeln(MemberChains[i]);
  }
}
*/

/*
execute CalculateMemberCombinationCount {
  for (var i=3;i<=MemberNo;i++) {
    var CombinationCount = 1;
    for (var j=MemberNo;j>MemberNo-i;j--) {
      CombinationCount = CombinationCount*j
    }
    for (var k=1;k<=i;k++) {
      CombinationCount = CombinationCount / k;
    }
    writeln("Combination Count For Member Count ", i, " == ", CombinationCount);
  } 
}



execute GetNoRepetitionSequences {
  
  function discardBuiltinKeys(sparseArray) {
    var idx = 0;
    var newSparseArray = new Array();
    for (var i in sparseArray) {
      if ( i != 'toString' ) {
        if ( i != 'join') {
          if ( i != 'reverse') {
            if ( i != 'sort') {
              newSparseArray[idx] = sparseArray[i].split("");
      	      idx += 1;
      	    }
      	  }
      	}
      }
    }
    return newSparseArray;
  }
  
  function getCombinations(selectedMembers,selectedMemberCount,neededMember, combinations) {
    var lastestSelectedMember = 0;
    if (selectedMemberCount > 0) {
      lastestSelectedMember = selectedMembers[selectedMemberCount-1];
    }
    if (selectedMemberCount + 1 == neededMember) {
      // last round
      for (var j=lastestSelectedMember+1;j<=Opl.card(MemberSet);j++) {
        var newSelectedMembers = new Array();
        for (var k=0;k<=selectedMemberCount-1;k++) {
          newSelectedMembers[k] = selectedMembers[k];
        }
        newSelectedMembers[selectedMemberCount] = j;
        combinations[newSelectedMembers.join()] = newSelectedMembers.join("");
        //writeln("selected members ", newSelectedMembers.join());
      }
    } else {
      for (var j=lastestSelectedMember+1;j<=Opl.card(MemberSet);j++) {
        var newSelectedMembers = new Array();
        var newSelectedMemberCount = selectedMemberCount + 1;
        if ( lastestSelectedMember != 0) {
          for (var k=0;k<=selectedMemberCount-1;k++) {
          	newSelectedMembers[k] = selectedMembers[k];
          }
        }
        newSelectedMembers[selectedMemberCount] = j; 
        getCombinations(newSelectedMembers, newSelectedMemberCount, neededMember, combinations);
      }
    }
  }
  
  function getPermutations(selectedMembers,selectedMemberCount, residualMembers, neededMember, permutations) {
    if (selectedMemberCount + 1 == neededMember) {
      // last round
      var newSelectedMembers = new Array();
      for (var k=0;k<=selectedMemberCount-1;k++) {
        newSelectedMembers[k] = selectedMembers[k];
      }
      newSelectedMembers[selectedMemberCount] = residualMembers[0];
      permutations[newSelectedMembers.join()] = newSelectedMembers.join("");
      //writeln("permutation: ", newSelectedMembers.join());
    } else {
      for (var j=0;j<=residualMembers.length-1;j++) {
        var newSelectedMembers = new Array();
        var newResidualMembers = new Array();
        var newSelectedMemberCount = selectedMemberCount + 1;
        if ( selectedMemberCount != 0) {
          for (var k=0;k<=selectedMemberCount-1;k++) {
          	newSelectedMembers[k] = selectedMembers[k];
          }
        }
        newSelectedMembers[selectedMemberCount] = residualMembers[j];
        for (var l=0,m=0;l<=residualMembers.length-1;l++) {
          if (l != j) {
            newResidualMembers[m] = residualMembers[l];
            m += 1;
          }  
        }
        getPermutations(newSelectedMembers, newSelectedMemberCount, newResidualMembers, neededMember, permutations);
      }
    }
  }
  
  
  //var selectedMembers = new Array();
  //var allMembers = new Array(1, 2, 3);
  //var permutations = new Array();
  //getPermutations(selectedMembers, 0, allMembers, allMembers.length, permutations);
  
  
  function generateSequences(allMembers) {
    var sequences = new Array();
    var count = 0;
    var repetitions = allMembers.length - 2;
    for (var i=0;i<repetitions;i++) {
      // prefix 1,allMembers[i+1]
      //var movingMembers = new Array();
      var allMembersString = allMembers.join(""); 
      // get movingMembers
      var movingMembersString = (allMembersString.substring(1, i+1) + allMembersString.substring(i+2,allMembers.length-1)).substring(0,i);
      var movingMembers = movingMembersString.split("");
      // get residualMembers
      var residualMembersString = allMembersString.substring(1, i+1) + allMembersString.substring(i+2);
      var residualMembers = residualMembersString.split("");
      //writeln('prefix: ', prefix, ' moving members: ', movingMembers.join(), ' residual members: ', residualMembers.join());
      if ( residualMembers.length > 1) { 
        var permutations = new Array();
      	var selectedMembers = new Array();
      	getPermutations(selectedMembers, 0, residualMembers, residualMembers.length, permutations);
      	// discard 'toString', 'join', 'reverse', 'sort' element from permutations
      	var permutations = discardBuiltinKeys(permutations);
      	for (var p=0;p<=permutations.length-1;p++) {
      	  var endsWithMovingMember = 0;
      	  for (var l=0;l<=movingMembers.length-1;l++) {
      	    //if (permutations[p].charAt(residualMembers.length - 1) == movingMembers[l]) {
      	    if (permutations[p][residualMembers.length - 1] == movingMembers[l]) {
      	      endsWithMovingMember = 1;
      	    }
          }
          if ( endsWithMovingMember == 0) {
            sequences[count] = new Array(1, allMembers[i+1]);
            for (var j=0;j<permutations[p].length;j++) {
              sequences[count][j+2] = permutations[p][j];
            }
            count += 1;
          }
        }
      } else {
        sequences[0] = new Array(1, allMembers[i+1]);
        sequences[count][2] = residualMembers[0];
      }
    }
    return sequences;
  }
  
  
  //var allMembers = new Array(1, 2, 3, 4);
  //var sequences = new Array();
  //generateSequences(allMembers, sequences)
  //for (var i=0;i<=sequences.length-1;i++) {
  //  writeln(sequences[i]);
  //}
  //writeln('no repetition sequences: ', sequences.length);
  
  
  for (var neededMemberCount=3;neededMemberCount<=MemberNo;neededMemberCount++) {
    writeln('member count: ', neededMemberCount);
    // construct members
    var members = new Array();
    for (var i=0;i<=neededMemberCount-1;i++) {
      members[i] = i+1;
    }
    var sequences = generateSequences(members)
    
    //writeln('no repetition sequences: ', sequences.length);
    //for (var i=0;i<=sequences.length-1;i++) {
    //	writeln('sequence: ', sequences[i]);
    //}	
    
    var selectedMembers = new Array();
    var combinations = new Array();
  	getCombinations(selectedMembers, 0, neededMemberCount, combinations);
  	combinations = discardBuiltinKeys(combinations);
  	for (var i=0;i<=combinations.length-1;i++) {
  	  writeln('combination: ', combinations[i].join(""));
  	  for (var j=0;j<=sequences.length-1;j++) {
    	writeln('sequence: ', sequences[j].join(""));
    	var chain = new Array();
    	for (var k=0;k<=neededMemberCount-1;k++) {
    	  //writeln(combinations[i][sequences[j][k]-1]);
    	  chain[k] = combinations[i][sequences[j][k]-1];  
    	}
    	chain[neededMemberCount] = combinations[i][sequences[j][0]-1];
    	MemberChains.add(chain.join(""));	
      }	
  	}
  }
  
  for (var chain in MemberChains) {
    writeln('chain: ', chain);
  }
}
*/


minimize 0;