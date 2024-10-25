import torch
import torchvision
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import OkraClassifier


###### Hyperparameters ######

lr = 0.00001
batch_size = 1000    # This should be adjusted to what your GPU can handle
epochs = 15
load_existing_model = True
test_while_training = True

#############################


CUDA_VISIBLE_DEVICES=1

device = torch.device('cpu')

# Device
if torch.cuda.is_available():
    device = torch.device('cuda')
    print('Using device:', torch.cuda.get_device_name(device))
else:
    print('Warning: No CUDA device available')


# Disable Debugging APIs
torch.autograd.set_detect_anomaly(mode=False)
torch.autograd.profiler.emit_nvtx(enabled=False)
torch.autograd.profiler.profile(enabled=False)


def main():
    # Prepare data
    transform = transforms.Compose([transforms.ToTensor()])#, transforms.Normalize(mean=0.1307, std=0.3081)
    train = torchvision.datasets.MNIST('./data', train=True, download=True, transform=transform)
    test = torchvision.datasets.MNIST('./data', train=False, download=True, transform=transform)
    trainLoader = DataLoader(train, shuffle=True, batch_size=batch_size, num_workers=15)
    testLoader = DataLoader(test, shuffle=False, batch_size=batch_size, num_workers=15)
    # Prepare model
    weights_file = None
    if load_existing_model:
        weights_file = './okra.resnet.weights'
    model = OkraClassifier.get_model(weights_file, device.type)
    # Prepare Optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    # Prepare Loss Function
    loss_fn = torch.nn.CrossEntropyLoss()
    # Start training
    train_model(model, trainLoader, testLoader, optimizer, loss_fn)
    # Save the model
    resp = input('Save model? [y/n]')
    if resp == 'y':
        torch.save(model.state_dict(), f'okraE{epochs}.resnet.weights')


def train_model(model, trainData, testData, optimizer, loss_fn):
    for epoch in range(epochs):
        if test_while_training:
            accuracy = test(model, testData)
            print(f'Accuracy after epoch {epoch}: {accuracy:>0.2f}%')

        if epoch != 0 and epoch % 3 == 0:
            resp = input('Save model? [y/n]')
            if resp == 'y':
                torch.save(model.state_dict(), f'okraE{epoch}.resnet.weights')
            elif resp == 'q':
                return

        trainOneEpoch(model, trainData, optimizer, loss_fn)

    accuracy = test(model, testData)
    print(f'Accuracy after epoch {epochs}: {accuracy:>0.2f}%')


def trainOneEpoch(model, data, optimizer, loss_fn):
    model.train()
    for x_batch, y_batch in data:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        #x_batch = x_batch.view(x_batch.shape[0], -1)
        pred = model(x_batch)
        loss = loss_fn(pred, y_batch)

        # This method is more efficient than zero_grad()
        # because it does not waste time overwriting
        # the gradients with zeros
        for param in model.parameters():
            param.grad = None

        loss.backward()
        optimizer.step()


def test(model, data):
    model.eval()
    correct = 0
    size = float(len(data.dataset))
    with torch.no_grad():
        for x_batch, y_batch in data:
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)
            #x_batch = x_batch.view(x_batch.shape[0], -1)
            pred = model(x_batch)
            correct += (torch.argmax(pred, 1) == y_batch).float().sum().item()

    return (correct / size) * 100


if __name__=="__main__":
    main()

