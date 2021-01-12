We present an extended version of the prolexa_plus framework whereby functionality is augmented with the introduction of a common sense reasoning though the aquisition of common sense knowledge. We connect Prolex Plus to [ConceptNet](http://conceptnet.io), a freely available large-scale commonsense knowledge base, which  provides prolexa with the necessary semantic knowledge to enable deeper and more meaningful understanding of textual information. Thus, ConceptNet empowers it to perform contextual common sense reasoning, positioning new information and rules in the context of stored knowledge.

When a user inserts a statement, prolexa communicates with the external database and fetches additional knowledge based on the intput. For example, if it receives an input: "Helen is a doctor", it can access the concept database and summise that Helen is also a: "medic", a "person of science" and a "professional". 
Currently, the relationships that we achieve fall under the following classes:

```python
class REL(Enum):
    IS_A = 'IsA'
    HAS_A = 'HasA'
    PART_OF = 'PartOF'
    USED_FOR = 'UsedFor'
    CAPABLE_OF = 'CapableOf'
    AT_LOCATION = 'AtLocation'
    CAUSES = 'Causes'
    HAS_PROPERTY = 'HasProperty'
    DESIRES = 'Desires'
    CREATED_BY = 'CreatedBy'
    CAUSES_DESIRE = 'CausesDesire'
    MADE_OF = 'MadeOf'
```
Currently, we only fetch the common sense knowledge pertaining to simple nouns (e.g. ...), but this can be easily edited to account for adjectives, verbs, noun phrases etc. 

Next, for each of these relations, we construct a prolog rule and update prolexa's stored rules file (prolexa.pl). However, in order to access the natural language interface, we must define a grammar for each category of rules (e.g. has a.., capable of..., is a...). 

The new functionality can be used to address the type of questions and riddles posed in Option 1 of this coursework. For example: 

If someone is medic then they can care

if someone is a doctor then they are a worker

Arthur is a doctor

Bill is a worker
 
Arthur is a worker?

Bill is a doctor?

(This can be shown via demonstration).


While prolexa can handle any rule with the prefix "is a type of...", it was necessary to also extend its grammar to permit it to take advantage of all knowledge provided by Conceptnet. For example, prolexa should handle such statements as "every doctor has a hammer" and "every teacher is is capable of teaching". Prolexa now understands such statements, however the complexity of the responses stored in conceptnet hinders its ability to fully process them and return reasoned responses. 

Thus, future work should insert more complex structures into Prolexa's grammer to ensure access to the entire knowledge database. The next version should incoporate additional rules such as (at location, mad of..., used for...., etc.). 

### Example entry
```shell
> tell me about peter 
*** utterance(tell me about peter)
*** goal(all_answers(peter,_37958))
*** answer(peter is human. peter is mortal)
peter is human. peter is mortal

> peter is a teacher 
*** utterance(peter is a teacher)
*** rule([(teacher(peter):-true)])
*** answer(I will remember that peter is a teacher)
*** answer(I heard you say,  peter is a teacher , could you rephrase that please?)
Acquiring common sense knowledge ...
Rules were added successfully!
I will remember that peter is a teacher
I have also discovered more knowledge about peter

[3:29 PM] Kevin Kermani Nejad
> tell me about peter 
*** utterance(tell me about peter)
*** goal(all_answers(peter,_37958))
*** answer(peter is human. peter is mortal)
peter is human. peter is mortal

> peter is a teacher 
*** utterance(peter is a teacher)
*** rule([(teacher(peter):-true)])
*** answer(I will remember that peter is a teacher)
*** answer(I heard you say,  peter is a teacher , could you rephrase that please?)
Acquiring common sense knowledge ...
Rules were added successfully!
I will remember that peter is a teacher
I have also discovered more knowledge about peter

> explain why peter is a educator 
*** utterance(explain why peter is a educator)
*** goal(explain_question(educator(peter),_54722,_54466))
*** answer(peter is a teacher; every teacher is a educator; therefore peter is a educator)
peter is a teacher; every teacher is a educator; therefore peter is a educator
```





