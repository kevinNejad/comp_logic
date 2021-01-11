We present an extended version of the prolexa_plus framework whereby functionality is augmented with the introduction of a database containing common sense knowledge. We connect Prolex Plus to ConceptNet, a freely available large-scale commonsense knowledge base, which  provides prolexa with the necessary semantic knowledge to enable deeper and more meaningful understanding of textual information. Thus, conceptnet empowers it to perform contextual common sense reasoning, positioning new information and rules in the context of stored knowledge.

When a user inserts a statement, prolexa communicates with the external database and fetches additional knowledge based on the intput. For example, if it receives an input: "Helen is a doctor", it can access the concept database and summise that Helen is also a: "medic", a "person of science" and a "professional". 


The new functionality can be used to address the type of questions and riddles posed in Option 1 of this coursework. For example: 
If someone is medic then they can care

if someone is a doctor then they are a worker

Arthur is a doctor

Bill is a worker
 
Arthur is a worker?

Bill is a doctor?

(This can be shown via demonstration).

While prolexa can handle any rule with the prefix "is a type of...", it was necessary to also extend its grammar to permit it to take advantage of all knowledge provided by Conceptnet. For example, prolexa should hanle such as "every doctor has a hammer" and "every teacher is is capable of teaching". Prolexa now understands such statements, however the complexity of the responses stored in conceptnet hinders its ability to fully process them and return reasoned responses. Thus, future work should insert more complex structures into Prolexa's grammer to ensure access to the entire knowledge database. 
