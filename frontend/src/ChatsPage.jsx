import { PrettyChatWindow } from "react-chat-engine-pretty";


const ChatsPage = (props) => {
  return (
    <div className="background">
      <PrettyChatWindow
        projectId={"project id here"}
        username={props.user.username}
        secret={props.user.secret}
      />
    </div>
  );
};

export default ChatsPage;